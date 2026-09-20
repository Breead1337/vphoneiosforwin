/*
 * vr-apv-fb: Software framebuffer replacing Apple's PVG (ParavirtualizedGraphics)
 *
 * The iOS guest talks to two MMIO regions:
 *   apv-gfx  @ 0x30200000 (64 KB) — display control / status & command ring
 *   apv-iosfc @ 0x30210000 (64 KB) — IOSurface configuration
 *
 * Instead of delegating to macOS PGDevice/PGIOSurfaceHostDevice (impossible
 * on Windows/Linux), we intercept the MMIO protocol, capture the guest's
 * framebuffer physical address, handle command ring submissions, and blit
 * from guest RAM into a QemuConsole as well as periodically saving screenshots.
 *
 * SPDX-License-Identifier: GPL-2.0-or-later
 */

#include "qemu/osdep.h"
#include "qemu/log.h"
#include "qemu/module.h"
#include "qemu/timer.h"
#include "hw/irq.h"
#include "hw/qdev-properties.h"
#include "hw/sysbus.h"
#include "ui/console.h"
#include "ui/surface.h"
#include "exec/cpu-common.h"
#include "system/address-spaces.h"
#include "qapi/error.h"
#include "qom/object.h"

/* ---------- configurable defaults (guest may override via MMIO) ---------- */
#define APV_DEFAULT_WIDTH   1024
#define APV_DEFAULT_HEIGHT  1024
#define APV_BPP             4        /* BGRA-8888 */
#define APV_REFRESH_MS      33       /* ~30 fps */

/* ---------- IOSFC register offsets (guest writes surface info here) ------ */
#define IOSFC_SURFACE0_BASE     0x1000   /* phys addr of surface buffer 0 */
#define IOSFC_SURFACE0_PAGES    0x1008   /* page count (4 KB pages) */
#define IOSFC_SURFACE1_BASE     0x1010   /* phys addr of surface buffer 1 */
#define IOSFC_SURFACE1_PAGES    0x1018   /* page count for surface 1 */
#define IOSFC_STRIDE            0x1020   /* bytes per row (if provided) */
#define IOSFC_STATUS            0x0000   /* status / handshake */
#define IOSFC_READ_1028         0x1028   /* status register read by guest */

/* ---------- GFX register offsets (guest reads status, writes commands) --- */
#define GFX_CTRL                0x1000   /* control / enable register */
#define GFX_RING_LEN            0x1004   /* primary ring buffer length */
#define GFX_RING_HEAD           0x1008   /* producer head pointer */
#define GFX_RING_TAIL           0x100c   /* consumer tail pointer */
#define GFX_RING2_LEN           0x1010   /* secondary ring buffer length */
#define GFX_STATUS_A            0x1014   /* status register A */
#define GFX_STATUS_B            0x1018   /* status register B */
#define GFX_RING_PAGE           0x101c   /* primary ring base page */
#define GFX_STATUS_102C         0x102c   /* status register read by guest */
#define GFX_RING2_PAGE          0x1030   /* secondary ring base page */
#define GFX_CMD                 0x1034   /* command register */
#define GFX_READ_122C           0x122c   /* channel status read by guest */
#define GFX_READ_1234           0x1234   /* channel status read by guest */

/* Status values that the guest expects to see */
#define GFX_STATUS_READY        0x0      /* 0 = no error / ready */

#define TYPE_VR_APV_FB "vr-apv-fb"
OBJECT_DECLARE_SIMPLE_TYPE(VrApvFbState, VR_APV_FB)

typedef struct VrApvFbSurface {
    hwaddr phys_base;       /* guest physical address */
    uint32_t page_count;    /* number of 4 KB pages */
} VrApvFbSurface;

struct VrApvFbState {
    SysBusDevice parent_obj;

    /* MMIO regions */
    MemoryRegion iomem_gfx;
    MemoryRegion iomem_iosfc;

    /* IRQ lines */
    qemu_irq irq_gfx;
    qemu_irq irq_iosfc;

    /* Display */
    QemuConsole *con;
    QEMUTimer *refresh_timer;

    /* Guest surface info (captured from IOSFC writes) */
    VrApvFbSurface surfaces[2];
    int active_surface;     /* which surface to display (0 or 1) */
    uint32_t stride;        /* bytes per row */
    uint32_t width;
    uint32_t height;
    bool surface_configured; /* true once guest provides a valid surface */

    /* GFX command ring state */
    uint32_t gfx_ctrl;
    uint32_t gfx_cmd;
    uint32_t ring_len;
    uint32_t ring_head;
    uint32_t ring_tail;
    uint32_t ring_page;
    uint32_t ring2_len;
    uint32_t ring2_page;

    /* IOSFC state */
    uint32_t iosfc_status;

    /* Screenshot throttling & non-zero detection */
    int64_t last_ppm_dump_ms;
    bool has_rendered_content;
};

/* ======================================================================== */
/*  IOSFC MMIO (IOSurface configuration)                                    */
/* ======================================================================== */

static uint64_t iosfc_read(void *opaque, hwaddr offset, unsigned size)
{
    VrApvFbState *s = opaque;
    uint64_t val = 0;

    switch (offset) {
    case IOSFC_STATUS:
        val = s->iosfc_status;
        break;
    case IOSFC_SURFACE0_BASE:
        val = s->surfaces[0].phys_base;
        break;
    case IOSFC_SURFACE0_PAGES:
        val = s->surfaces[0].page_count;
        break;
    case IOSFC_SURFACE1_BASE:
        val = s->surfaces[1].phys_base;
        break;
    case IOSFC_SURFACE1_PAGES:
        val = s->surfaces[1].page_count;
        break;
    case IOSFC_STRIDE:
        val = s->stride;
        break;
    case IOSFC_READ_1028:
        val = 0;
        break;
    default:
        qemu_log_mask(LOG_UNIMP,
                      "vr-apv-fb: iosfc read  offset=0x%04" HWADDR_PRIx
                      " size=%u → 0\n", offset, size);
        break;
    }

    return val;
}

static void iosfc_reconfigure(VrApvFbState *s)
{
    uint64_t total_bytes;

    if (!s->surfaces[0].phys_base || !s->surfaces[0].page_count) {
        return;
    }

    total_bytes = (uint64_t)s->surfaces[0].page_count * 4096;

    /*
     * If stride was explicitly provided, use it; otherwise derive from
     * buffer size assuming common iOS display resolutions.
     */
    if (s->stride == 0) {
        if (total_bytes >= (uint64_t)1920 * 1080 * APV_BPP) {
            s->width  = 1920;
            s->height = 1080;
            s->stride = s->width * APV_BPP;
        } else {
            /* 1024 pages = 4MB = 1024x1024x4 */
            s->width  = 1024;
            s->stride = s->width * APV_BPP;
            s->height = (uint32_t)(total_bytes / s->stride);
            if (s->height == 0) {
                s->height = 1024;
            }
        }
    } else {
        s->width = s->stride / APV_BPP;
        if (s->width == 0) {
            s->width = 1024;
        }
        s->height = (uint32_t)(total_bytes / s->stride);
        if (s->height == 0) {
            s->height = 1024;
        }
    }

    qemu_log("vr-apv-fb: configured surface %ux%u stride=%u "
             "phys=0x%" HWADDR_PRIx " (%u pages)\n",
             s->width, s->height, s->stride,
             s->surfaces[0].phys_base,
             s->surfaces[0].page_count);

    qemu_console_resize(s->con, s->width, s->height);
    s->surface_configured = true;

    /* Pulse IOSFC IRQ to ack the surface mapping */
    qemu_irq_pulse(s->irq_iosfc);
}

static void iosfc_write(void *opaque, hwaddr offset, uint64_t val, unsigned size)
{
    VrApvFbState *s = opaque;

    switch (offset) {
    case IOSFC_STATUS:
        s->iosfc_status = val;
        break;

    case IOSFC_SURFACE0_BASE:
        s->surfaces[0].phys_base = val;
        qemu_log("vr-apv-fb: surface[0].base = 0x%" PRIx64 "\n", val);
        iosfc_reconfigure(s);
        break;

    case IOSFC_SURFACE0_PAGES:
        s->surfaces[0].page_count = val;
        qemu_log("vr-apv-fb: surface[0].pages = %" PRIu64 " (%" PRIu64 " bytes)\n",
                 val, val * 4096);
        iosfc_reconfigure(s);
        break;

    case IOSFC_SURFACE1_BASE:
        s->surfaces[1].phys_base = val;
        qemu_log("vr-apv-fb: surface[1].base = 0x%" PRIx64 "\n", val);
        break;

    case IOSFC_SURFACE1_PAGES:
        s->surfaces[1].page_count = val;
        break;

    case IOSFC_STRIDE:
        s->stride = val;
        qemu_log("vr-apv-fb: stride = %" PRIu64 " bytes\n", val);
        iosfc_reconfigure(s);
        break;

    default:
        qemu_log_mask(LOG_UNIMP,
                      "vr-apv-fb: iosfc write offset=0x%04" HWADDR_PRIx
                      " val=0x%" PRIx64 " UNHANDLED\n", offset, val);
        break;
    }
}

static const MemoryRegionOps iosfc_ops = {
    .read  = iosfc_read,
    .write = iosfc_write,
    .endianness = DEVICE_LITTLE_ENDIAN,
    .valid.min_access_size = 4,
    .valid.max_access_size = 8,
    .impl.min_access_size  = 4,
    .impl.max_access_size  = 8,
};

/* ======================================================================== */
/*  GFX MMIO (display control / status & command ring)                      */
/* ======================================================================== */

static uint64_t gfx_read(void *opaque, hwaddr offset, unsigned size)
{
    VrApvFbState *s = opaque;
    uint64_t val = 0;

    switch (offset) {
    case GFX_CTRL:
        val = s->gfx_ctrl;
        break;
    case GFX_RING_LEN:
        val = s->ring_len;
        break;
    case GFX_RING_HEAD:
        val = s->ring_head;
        break;
    case GFX_RING_TAIL:
        /* Return consumer tail pointer: acknowledge all commands up to head */
        val = s->ring_tail;
        break;
    case GFX_RING2_LEN:
        val = s->ring2_len;
        break;
    case GFX_STATUS_A:
        val = GFX_STATUS_READY;
        break;
    case GFX_STATUS_B:
        val = GFX_STATUS_READY;
        break;
    case GFX_RING_PAGE:
        val = s->ring_page;
        break;
    case GFX_STATUS_102C:
        val = 0;
        break;
    case GFX_RING2_PAGE:
        val = s->ring2_page;
        break;
    case GFX_CMD:
        val = s->gfx_cmd;
        break;
    case GFX_READ_122C:
        val = 0;
        break;
    case GFX_READ_1234:
        val = 0;
        break;
    default:
        qemu_log_mask(LOG_UNIMP,
                      "vr-apv-fb: gfx read  offset=0x%04" HWADDR_PRIx
                      " size=%u → 0\n", offset, size);
        break;
    }

    return val;
}

static void gfx_write(void *opaque, hwaddr offset, uint64_t val, unsigned size)
{
    VrApvFbState *s = opaque;

    switch (offset) {
    case GFX_CTRL:
        s->gfx_ctrl = val;
        qemu_log("vr-apv-fb: GFX_CTRL = 0x%" PRIx64 "\n", val);
        break;

    case GFX_RING_LEN:
        s->ring_len = val;
        qemu_log("vr-apv-fb: GFX_RING_LEN = 0x%" PRIx64 "\n", val);
        break;

    case GFX_RING_HEAD:
        s->ring_head = val;
        /*
         * Guest submitted commands up to 'val' in the ring buffer.
         * Immediately acknowledge consumption by updating tail to head,
         * and pulse GFX IRQ to notify the guest driver.
         */
        s->ring_tail = val;
        qemu_irq_pulse(s->irq_gfx);
        break;

    case GFX_RING_TAIL:
        s->ring_tail = val;
        break;

    case GFX_RING2_LEN:
        s->ring2_len = val;
        qemu_log("vr-apv-fb: GFX_RING2_LEN = 0x%" PRIx64 "\n", val);
        break;

    case GFX_RING_PAGE:
        s->ring_page = val;
        qemu_log("vr-apv-fb: GFX_RING_PAGE = 0x%" PRIx64 "\n", val);
        break;

    case GFX_RING2_PAGE:
        s->ring2_page = val;
        qemu_log("vr-apv-fb: GFX_RING2_PAGE = 0x%" PRIx64 "\n", val);
        break;

    case GFX_CMD:
        s->gfx_cmd = val;
        qemu_log("vr-apv-fb: GFX_CMD = 0x%" PRIx64 "\n", val);
        /* Ack command with an IRQ pulse */
        qemu_irq_pulse(s->irq_gfx);
        break;

    default:
        qemu_log_mask(LOG_UNIMP,
                      "vr-apv-fb: gfx write offset=0x%04" HWADDR_PRIx
                      " val=0x%" PRIx64 " UNHANDLED\n", offset, val);
        break;
    }
}

static const MemoryRegionOps gfx_ops = {
    .read  = gfx_read,
    .write = gfx_write,
    .endianness = DEVICE_LITTLE_ENDIAN,
    .valid.min_access_size = 4,
    .valid.max_access_size = 8,
    .impl.min_access_size  = 4,
    .impl.max_access_size  = 8,
};

/* ======================================================================== */
/*  Display update & Framebuffer capture                                    */
/* ======================================================================== */

static void dump_ppm_screenshot(const char *path, const uint32_t *src,
                                uint32_t width, uint32_t height, uint32_t stride)
{
    FILE *f = fopen(path, "wb");
    if (!f) {
        return;
    }

    fprintf(f, "P6\n%u %u\n255\n", width, height);
    for (uint32_t y = 0; y < height; y++) {
        const uint32_t *row = (const uint32_t *)((const uint8_t *)src + y * stride);
        for (uint32_t x = 0; x < width; x++) {
            uint32_t px = row[x];
            uint8_t rgb[3];
            /* BGRA LE -> RGB */
            rgb[0] = (px >> 16) & 0xFF; /* R */
            rgb[1] = (px >> 8)  & 0xFF; /* G */
            rgb[2] = px         & 0xFF; /* B */
            fwrite(rgb, 1, 3, f);
        }
    }
    fclose(f);
}

static void apv_fb_update(void *opaque)
{
    VrApvFbState *s = opaque;
    DisplaySurface *surface;
    hwaddr fb_phys;
    uint32_t fb_size;
    void *guest_fb;
    hwaddr mapped_len;
    uint32_t *dst;
    const uint32_t *src;
    uint32_t row, col;
    bool nonzero = false;
    int64_t now_ms;

    if (!s->surface_configured || s->width == 0 || s->height == 0) {
        return;
    }

    surface = qemu_console_surface(s->con);
    if (!surface) {
        return;
    }

    fb_phys = s->surfaces[s->active_surface].phys_base;
    if (!fb_phys) {
        return;
    }

    fb_size = s->height * s->stride;
    mapped_len = fb_size;

    guest_fb = cpu_physical_memory_map(fb_phys, &mapped_len, false);
    if (!guest_fb || mapped_len < fb_size) {
        if (guest_fb) {
            cpu_physical_memory_unmap(guest_fb, mapped_len, false, 0);
        }
        return;
    }

    dst = (uint32_t *)surface_data(surface);
    src = (const uint32_t *)guest_fb;

    /* Blit guest BGRA-8888 -> host XRGB-8888 and detect rendered pixels */
    for (row = 0; row < s->height; row++) {
        const uint32_t *srow = (const uint32_t *)((const uint8_t *)src + row * s->stride);
        uint32_t *drow = dst + row * s->width;
        for (col = 0; col < s->width; col++) {
            uint32_t pix = srow[col];
            if (pix != 0) {
                nonzero = true;
            }
            drow[col] = pix | 0xFF000000;
        }
    }

    now_ms = qemu_clock_get_ms(QEMU_CLOCK_REALTIME);
    if (nonzero && (!s->has_rendered_content || (now_ms - s->last_ppm_dump_ms > 2000))) {
        s->has_rendered_content = true;
        s->last_ppm_dump_ms = now_ms;
        qemu_log("vr-apv-fb: NON-ZERO PIXELS DETECTED! Saving /home/ard/vrwork/framebuffer.ppm (%ux%u)\n",
                 s->width, s->height);
        dump_ppm_screenshot("/home/ard/vrwork/framebuffer.ppm", src, s->width, s->height, s->stride);
    }

    cpu_physical_memory_unmap(guest_fb, mapped_len, false, 0);
    dpy_gfx_update_full(s->con);
}

static void apv_fb_timer_tick(void *opaque)
{
    VrApvFbState *s = opaque;

    apv_fb_update(s);
    timer_mod(s->refresh_timer,
              qemu_clock_get_ms(QEMU_CLOCK_REALTIME) + APV_REFRESH_MS);
}

static void apv_fb_invalidate(void *opaque)
{
    (void)opaque;
}

static const GraphicHwOps apv_fb_ops = {
    .invalidate  = apv_fb_invalidate,
    .gfx_update  = apv_fb_update,
};

/* ======================================================================== */
/*  Device lifecycle                                                        */
/* ======================================================================== */

static void apv_fb_realize(DeviceState *dev, Error **errp)
{
    VrApvFbState *s = VR_APV_FB(dev);

    /* GFX MMIO region — 64 KB */
    memory_region_init_io(&s->iomem_gfx, OBJECT(dev), &gfx_ops,
                          s, "vr-apv-gfx", 0x10000);
    sysbus_init_mmio(SYS_BUS_DEVICE(dev), &s->iomem_gfx);

    /* IOSFC MMIO region — 64 KB */
    memory_region_init_io(&s->iomem_iosfc, OBJECT(dev), &iosfc_ops,
                          s, "vr-apv-iosfc", 0x10000);
    sysbus_init_mmio(SYS_BUS_DEVICE(dev), &s->iomem_iosfc);

    /* Two IRQ lines: 0 = GFX (SPI 0x11), 1 = IOSFC (SPI 0x10) */
    sysbus_init_irq(SYS_BUS_DEVICE(dev), &s->irq_gfx);
    sysbus_init_irq(SYS_BUS_DEVICE(dev), &s->irq_iosfc);

    /* Initial state */
    s->width  = APV_DEFAULT_WIDTH;
    s->height = APV_DEFAULT_HEIGHT;
    s->stride = APV_DEFAULT_WIDTH * APV_BPP;
    s->active_surface = 0;
    s->surface_configured = false;
    s->last_ppm_dump_ms = 0;
    s->has_rendered_content = false;

    /* Create a QEMU display console */
    s->con = graphic_console_init(dev, 0, &apv_fb_ops, s);
    qemu_console_resize(s->con, s->width, s->height);

    /* Independent periodic refresh timer at ~30 FPS */
    s->refresh_timer = timer_new_ms(QEMU_CLOCK_REALTIME, apv_fb_timer_tick, s);
    timer_mod(s->refresh_timer,
              qemu_clock_get_ms(QEMU_CLOCK_REALTIME) + APV_REFRESH_MS);

    qemu_log("vr-apv-fb: realized, initial display %ux%u with 30fps refresh timer\n",
             s->width, s->height);
}

static void apv_fb_class_init(ObjectClass *oc, const void *data)
{
    DeviceClass *dc = DEVICE_CLASS(oc);

    dc->realize = apv_fb_realize;
    set_bit(DEVICE_CATEGORY_DISPLAY, dc->categories);
    dc->desc = "VResearch APV Software Framebuffer (replaces PVG)";
}

static const TypeInfo apv_fb_info = {
    .name          = TYPE_VR_APV_FB,
    .parent        = TYPE_SYS_BUS_DEVICE,
    .instance_size = sizeof(VrApvFbState),
    .class_init    = apv_fb_class_init,
};

static void apv_fb_register_types(void)
{
    type_register_static(&apv_fb_info);
}

type_init(apv_fb_register_types)
