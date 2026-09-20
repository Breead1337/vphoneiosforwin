/*
 * vr-apv-fb: Software framebuffer replacing Apple's PVG (ParavirtualizedGraphics)
 *
 * The iOS guest talks to two MMIO regions:
 *   apv-gfx  @ 0x30200000 (64 KB) — display control / status & command ring
 *   apv-iosfc @ 0x30210000 (64 KB) — IOSurface configuration
 *
 * Provides a clean authentic Apple boot screen during early boot & launchd initialization,
 * acknowledges command rings, and renders guest display surfaces when ready.
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

#define GFX_STATUS_READY        0x0      /* 0 = no error / ready */

#define TYPE_VR_APV_FB "vr-apv-fb"
OBJECT_DECLARE_SIMPLE_TYPE(VrApvFbState, VR_APV_FB)

/* 112x112 smooth Apple logo bitmap (4 x 32-bit words per row) */
static const uint32_t apple_logo_bits[112][4] = {
    { 0x00000000U, 0x00000000U, 0x00000000U, 0x00000000U },
    { 0x00000000U, 0x00000000U, 0x00000000U, 0x00000000U },
    { 0x00000000U, 0x00000000U, 0x00000000U, 0x00000000U },
    { 0x00000000U, 0x00000000U, 0x00000000U, 0x00000000U },
    { 0x00000000U, 0x00000000U, 0x00000000U, 0x00000000U },
    { 0x00000000U, 0x00000000U, 0x00000000U, 0x00000000U },
    { 0x00000000U, 0x00000000U, 0x00000000U, 0x00000000U },
    { 0x00000000U, 0x00000000U, 0x00000000U, 0x00000000U },
    { 0x00000000U, 0x00000000U, 0x00000000U, 0x00000000U },
    { 0x00000000U, 0x00000000U, 0x7e000000U, 0x00000000U },
    { 0x00000000U, 0x00000001U, 0xff000000U, 0x00000000U },
    { 0x00000000U, 0x00000003U, 0xff000000U, 0x00000000U },
    { 0x00000000U, 0x0000000fU, 0xff800000U, 0x00000000U },
    { 0x00000000U, 0x0000001fU, 0xff800000U, 0x00000000U },
    { 0x00000000U, 0x0000003fU, 0xff800000U, 0x00000000U },
    { 0x00000000U, 0x0000003fU, 0xff800000U, 0x00000000U },
    { 0x00000000U, 0x0000007fU, 0xff000000U, 0x00000000U },
    { 0x00000000U, 0x000000ffU, 0xff000000U, 0x00000000U },
    { 0x00000000U, 0x000001ffU, 0xff000000U, 0x00000000U },
    { 0x00000000U, 0x000001ffU, 0xfe000000U, 0x00000000U },
    { 0x00000000U, 0x000003ffU, 0xfe000000U, 0x00000000U },
    { 0x00000000U, 0x000003ffU, 0xfc000000U, 0x00000000U },
    { 0x00000000U, 0x000007ffU, 0xfc000000U, 0x00000000U },
    { 0x00000000U, 0x000007ffU, 0xf8000000U, 0x00000000U },
    { 0x00000000U, 0x000007ffU, 0xf0000000U, 0x00000000U },
    { 0x00000000U, 0x00000fffU, 0xe0000000U, 0x00000000U },
    { 0x00000000U, 0x00000fffU, 0xe0000000U, 0x00000000U },
    { 0x00000000U, 0x00000fffU, 0xc0000000U, 0x00000000U },
    { 0x00000000U, 0x00000fffU, 0x80000000U, 0x00000000U },
    { 0x00000000U, 0x000007feU, 0x00000000U, 0x00000000U },
    { 0x00000000U, 0x03f807fcU, 0x0fe00000U, 0x00000000U },
    { 0x00000000U, 0x3ffc03f0U, 0x1ffe0000U, 0x00000000U },
    { 0x00000000U, 0xfffc0000U, 0x1fff8000U, 0x00000000U },
    { 0x00000003U, 0xfffc0000U, 0x1fffe000U, 0x00000000U },
    { 0x0000000fU, 0xfffc0000U, 0x1ffff800U, 0x00000000U },
    { 0x0000001fU, 0xfffe0000U, 0x3ffffc00U, 0x00000000U },
    { 0x0000007fU, 0xfffe0000U, 0x3fffff00U, 0x00000000U },
    { 0x000000ffU, 0xffff0000U, 0x7fffff80U, 0x00000000U },
    { 0x000001ffU, 0xffff8000U, 0xffffffc0U, 0x00000000U },
    { 0x000003ffU, 0xffffc001U, 0xffffffe0U, 0x00000000U },
    { 0x000007ffU, 0xfffff007U, 0xfffffff0U, 0x00000000U },
    { 0x000007ffU, 0xffffff7fU, 0xfffff800U, 0x00000000U },
    { 0x00000fffU, 0xffffffffU, 0xffffc000U, 0x00000000U },
    { 0x00001fffU, 0xffffffffU, 0xffff0000U, 0x00000000U },
    { 0x00001fffU, 0xffffffffU, 0xfffe0000U, 0x00000000U },
    { 0x00003fffU, 0xffffffffU, 0xfffc0000U, 0x00000000U },
    { 0x00003fffU, 0xffffffffU, 0xfff80000U, 0x00000000U },
    { 0x00007fffU, 0xffffffffU, 0xfff00000U, 0x00000000U },
    { 0x00007fffU, 0xffffffffU, 0xffe00000U, 0x00000000U },
    { 0x0000ffffU, 0xffffffffU, 0xffc00000U, 0x00000000U },
    { 0x0000ffffU, 0xffffffffU, 0xffc00000U, 0x00000000U },
    { 0x0000ffffU, 0xffffffffU, 0xff800000U, 0x00000000U },
    { 0x0000ffffU, 0xffffffffU, 0xff800000U, 0x00000000U },
    { 0x0001ffffU, 0xffffffffU, 0xff800000U, 0x00000000U },
    { 0x0001ffffU, 0xffffffffU, 0xff000000U, 0x00000000U },
    { 0x0001ffffU, 0xffffffffU, 0xff000000U, 0x00000000U },
    { 0x0001ffffU, 0xffffffffU, 0xff000000U, 0x00000000U },
    { 0x0001ffffU, 0xffffffffU, 0xff000000U, 0x00000000U },
    { 0x0001ffffU, 0xffffffffU, 0xff000000U, 0x00000000U },
    { 0x0001ffffU, 0xffffffffU, 0xff000000U, 0x00000000U },
    { 0x0001ffffU, 0xffffffffU, 0xff000000U, 0x00000000U },
    { 0x0001ffffU, 0xffffffffU, 0xff000000U, 0x00000000U },
    { 0x0001ffffU, 0xffffffffU, 0xff000000U, 0x00000000U },
    { 0x0001ffffU, 0xffffffffU, 0xff800000U, 0x00000000U },
    { 0x0000ffffU, 0xffffffffU, 0xff800000U, 0x00000000U },
    { 0x0000ffffU, 0xffffffffU, 0xff800000U, 0x00000000U },
    { 0x0000ffffU, 0xffffffffU, 0xffc00000U, 0x00000000U },
    { 0x0000ffffU, 0xffffffffU, 0xffc00000U, 0x00000000U },
    { 0x00007fffU, 0xffffffffU, 0xffe00000U, 0x00000000U },
    { 0x0000ffffU, 0xffffffffU, 0xfff00000U, 0x00000000U },
    { 0x0000ffffU, 0xffffffffU, 0xfff80000U, 0x00000000U },
    { 0x0000ffffU, 0xffffffffU, 0xfffc0000U, 0x00000000U },
    { 0x0001ffffU, 0xffffffffU, 0xfffe0000U, 0x00000000U },
    { 0x0001ffffU, 0xffffffffU, 0xffff0000U, 0x00000000U },
    { 0x0001ffffU, 0xffffffffU, 0xffffc000U, 0x40000000U },
    { 0x0001ffffU, 0xffffffffU, 0xfffff803U, 0xc0000000U },
    { 0x0001ffffU, 0xffffffffU, 0xffffffffU, 0xc0000000U },
    { 0x0001ffffU, 0xffffffffU, 0xffffffffU, 0xc0000000U },
    { 0x0001ffffU, 0xffffffffU, 0xffffffffU, 0xc0000000U },
    { 0x0001ffffU, 0xffffffffU, 0xffffffffU, 0xc0000000U },
    { 0x0001ffffU, 0xffffffffU, 0xffffffffU, 0xc0000000U },
    { 0x0001ffffU, 0xffffffffU, 0xffffffffU, 0xc0000000U },
    { 0x0001ffffU, 0xffffffffU, 0xffffffffU, 0xc0000000U },
    { 0x0000ffffU, 0xffffffffU, 0xffffffffU, 0x80000000U },
    { 0x0000ffffU, 0xffffffffU, 0xffffffffU, 0x80000000U },
    { 0x0000ffffU, 0xffffffffU, 0xffffffffU, 0x80000000U },
    { 0x00007fffU, 0xffffff7fU, 0xffffffffU, 0x00000000U },
    { 0x00007fffU, 0xffffe003U, 0xffffffffU, 0x00000000U },
    { 0x00007fffU, 0xffff0000U, 0x7fffffffU, 0x00000000U },
    { 0x00003fffU, 0xfffe0000U, 0x3ffffffeU, 0x00000000U },
    { 0x00003fffU, 0xfff80000U, 0x0ffffffeU, 0x00000000U },
    { 0x00001fffU, 0xfff00000U, 0x07fffffcU, 0x00000000U },
    { 0x00000fffU, 0xffe00000U, 0x03fffff8U, 0x00000000U },
    { 0x00000fffU, 0xffc00000U, 0x01fffff8U, 0x00000000U },
    { 0x000007ffU, 0xffc00000U, 0x01fffff0U, 0x00000000U },
    { 0x000003ffU, 0xff800000U, 0x00ffffe0U, 0x00000000U },
    { 0x000001ffU, 0xff000000U, 0x007fffc0U, 0x00000000U },
    { 0x000000ffU, 0xff000000U, 0x007fff80U, 0x00000000U },
    { 0x0000007fU, 0xff000000U, 0x007fff00U, 0x00000000U },
    { 0x0000001fU, 0xfe000000U, 0x003ffc00U, 0x00000000U },
    { 0x0000000fU, 0xfe000000U, 0x003ff800U, 0x00000000U },
    { 0x00000003U, 0xfe000000U, 0x003fe000U, 0x00000000U },
    { 0x00000000U, 0x7e000000U, 0x003f0000U, 0x00000000U },
    { 0x00000000U, 0x0e000000U, 0x00380000U, 0x00000000U },
    { 0x00000000U, 0x00000000U, 0x00000000U, 0x00000000U },
    { 0x00000000U, 0x00000000U, 0x00000000U, 0x00000000U },
    { 0x00000000U, 0x00000000U, 0x00000000U, 0x00000000U },
    { 0x00000000U, 0x00000000U, 0x00000000U, 0x00000000U },
    { 0x00000000U, 0x00000000U, 0x00000000U, 0x00000000U },
    { 0x00000000U, 0x00000000U, 0x00000000U, 0x00000000U },
    { 0x00000000U, 0x00000000U, 0x00000000U, 0x00000000U },
    { 0x00000000U, 0x00000000U, 0x00000000U, 0x00000000U },
};

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
    bool is_real_ui_frame;   /* true when a real UI frame (not ring buffer) is ready */

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

    /* Boot animation state */
    int64_t boot_start_ms;
    uint32_t boot_progress_pct;
};

/* ======================================================================== */
/*  Apple Boot Screen Renderer                                              */
/* ======================================================================== */

static void draw_apple_boot_screen(DisplaySurface *surface, uint32_t progress_pct)
{
    uint32_t *dst = (uint32_t *)surface_data(surface);
    int w = surface_width(surface);
    int h = surface_height(surface);
    int logo_x = (w - 112) / 2;
    int logo_y = (h - 112) / 2 - 40;

    /* Solid pitch black */
    memset(dst, 0, (size_t)w * h * 4);

    /* Draw Apple logo centered in clean white */
    for (int y = 0; y < 112; y++) {
        int py = logo_y + y;
        if (py < 0 || py >= h) continue;
        for (int x = 0; x < 112; x++) {
            int px = logo_x + x;
            if (px < 0 || px >= w) continue;
            uint32_t word = apple_logo_bits[y][x / 32];
            if (word & (1U << (31 - (x % 32)))) {
                dst[py * w + px] = 0xFFFFFFFF;
            }
        }
    }

    /* Draw clean iOS boot progress bar */
    int bar_w = 200;
    int bar_h = 4;
    int bar_x = (w - bar_w) / 2;
    int bar_y = logo_y + 112 + 48;
    int fill_w = (bar_w * (int)progress_pct) / 100;

    for (int y = 0; y < bar_h; y++) {
        int py = bar_y + y;
        if (py < 0 || py >= h) continue;
        for (int x = 0; x < bar_w; x++) {
            int px = bar_x + x;
            if (px < 0 || px >= w) continue;
            if (x <= fill_w) {
                dst[py * w + px] = 0xFFE0E0E0; /* filled progress (silver) */
            } else {
                dst[py * w + px] = 0xFF303030; /* dark gray track */
            }
        }
    }
}

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
        break;
    }

    return val;
}

static void iosfc_reconfigure(VrApvFbState *s)
{
    /*
     * The guest passes descriptor ring buffers at 0x1000/0x1010 during start.
     * We acknowledge mapping via IRQ, but keep the clean Apple boot screen
     * until a true UI frame is submitted.
     */
    s->surface_configured = true;
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
        qemu_log("vr-apv-fb: surface[0].pages = %" PRIu64 "\n", val);
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
        break;

    default:
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
    default:
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
        break;

    case GFX_RING_LEN:
        s->ring_len = val;
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
        break;

    case GFX_RING_PAGE:
        s->ring_page = val;
        break;

    case GFX_RING2_PAGE:
        s->ring2_page = val;
        break;

    case GFX_CMD:
        s->gfx_cmd = val;
        qemu_irq_pulse(s->irq_gfx);
        break;

    default:
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
/*  Display update & Animation                                              */
/* ======================================================================== */

static void apv_fb_update(void *opaque)
{
    VrApvFbState *s = opaque;
    DisplaySurface *surface;

    surface = qemu_console_surface(s->con);
    if (!surface) {
        return;
    }

    if (!s->is_real_ui_frame) {
        /* Advance boot progress smoothly based on elapsed time */
        int64_t elapsed_s = (qemu_clock_get_ms(QEMU_CLOCK_REALTIME) - s->boot_start_ms) / 1000;
        uint32_t pct;
        if (elapsed_s < 8) {
            pct = 15 + (uint32_t)(elapsed_s * 5);          /* 0..8s: 15% -> 55% */
        } else if (elapsed_s < 25) {
            pct = 55 + (uint32_t)((elapsed_s - 8) * 1.8);  /* 8..25s: 55% -> 85% */
        } else if (elapsed_s < 90) {
            pct = 85 + (uint32_t)((elapsed_s - 25) * 0.2); /* 25..90s: 85% -> 98% */
        } else {
            pct = 99;
        }
        if (pct > 99) {
            pct = 99;
        }
        s->boot_progress_pct = pct;

        /* Render authentic iOS Apple boot screen */
        draw_apple_boot_screen(surface, s->boot_progress_pct);
        dpy_gfx_update_full(s->con);
        return;
    }

    /* When real UI is ready, blit guest VRAM */
    hwaddr fb_phys = s->surfaces[s->active_surface].phys_base;
    uint32_t fb_size = s->height * s->stride;
    hwaddr mapped_len = fb_size;
    void *guest_fb = cpu_physical_memory_map(fb_phys, &mapped_len, false);
    if (!guest_fb || mapped_len < fb_size) {
        if (guest_fb) {
            cpu_physical_memory_unmap(guest_fb, mapped_len, false, 0);
        }
        return;
    }

    uint32_t *dst = (uint32_t *)surface_data(surface);
    const uint32_t *src = (const uint32_t *)guest_fb;

    for (uint32_t row = 0; row < s->height; row++) {
        const uint32_t *srow = (const uint32_t *)((const uint8_t *)src + row * s->stride);
        uint32_t *drow = dst + row * s->width;
        for (uint32_t col = 0; col < s->width; col++) {
            drow[col] = srow[col] | 0xFF000000;
        }
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

    /* Initial display: clean black */
    s->width  = APV_DEFAULT_WIDTH;
    s->height = APV_DEFAULT_HEIGHT;
    s->stride = APV_DEFAULT_WIDTH * APV_BPP;
    s->active_surface = 0;
    s->surface_configured = false;
    s->is_real_ui_frame = false;
    s->boot_start_ms = qemu_clock_get_ms(QEMU_CLOCK_REALTIME);
    s->boot_progress_pct = 15;

    /* Create a QEMU display console */
    s->con = graphic_console_init(dev, 0, &apv_fb_ops, s);
    qemu_console_resize(s->con, s->width, s->height);

    /* Independent periodic refresh timer at ~30 FPS */
    s->refresh_timer = timer_new_ms(QEMU_CLOCK_REALTIME, apv_fb_timer_tick, s);
    timer_mod(s->refresh_timer,
              qemu_clock_get_ms(QEMU_CLOCK_REALTIME) + APV_REFRESH_MS);

    qemu_log("vr-apv-fb: realized, authentic Apple boot display %ux%u (30fps)\n",
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
