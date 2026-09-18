/*
 * vresearch101 SEP coprocessor mailbox (DT: iop-sep,vpiop @0x30250000).
 * Register file that latches writes; semantics filled in as reversed.
 *
 * SPDX-License-Identifier: GPL-2.0-or-later
 */

#include "qemu/osdep.h"
#include "qemu/log.h"
#include "hw/irq.h"
#include "hw/sysbus.h"
#include "hw/vmapple/vmapple.h"
#include "system/dma.h"

static void dump_ram(const char *tag, hwaddr addr, unsigned len)
{
    uint8_t buf[0x200];
    if (len > sizeof(buf)) {
        len = sizeof(buf);
    }
    if (dma_memory_read(&address_space_memory, addr, buf, len,
                        MEMTXATTRS_UNSPECIFIED) != MEMTX_OK) {
        qemu_log_mask(LOG_UNIMP, "sep-mbox: %s @%#" HWADDR_PRIx " unreadable\n", tag, addr);
        return;
    }
    for (unsigned i = 0; i < len; i += 16) {
        char line[3 * 16 + 1];
        int p = 0;
        for (unsigned j = 0; j < 16 && i + j < len; j++) {
            p += snprintf(line + p, sizeof(line) - p, "%02x ", buf[i + j]);
        }
        qemu_log_mask(LOG_UNIMP, "sep-mbox: %s %#06" HWADDR_PRIx ": %s\n", tag, addr + i, line);
    }
}

/* Snapshot the SEP scratch window and log 8-byte-aligned changes since last call. */
#define SNAP_BASE 0x70020000
#define SNAP_LEN  0xC000
static void diff_ram(const char *tag)
{
    static uint8_t *prev;
    uint8_t *cur = g_malloc(SNAP_LEN);

    if (dma_memory_read(&address_space_memory, SNAP_BASE, cur, SNAP_LEN,
                        MEMTXATTRS_UNSPECIFIED) != MEMTX_OK) {
        g_free(cur);
        return;
    }
    if (prev) {
        for (unsigned o = 0; o + 8 <= SNAP_LEN; o += 8) {
            uint64_t a, b;
            memcpy(&a, prev + o, 8);
            memcpy(&b, cur + o, 8);
            if (a != b) {
                qemu_log_mask(LOG_UNIMP,
                    "sep-mbox: %s %#010x: %016" PRIx64 " -> %016" PRIx64 "\n",
                    tag, SNAP_BASE + o, a, b);
            }
        }
        g_free(prev);
    }
    prev = cur;
}

OBJECT_DECLARE_SIMPLE_TYPE(VRSepMboxState, VR_SEP_MBOX)

#define MBOX_SIZE 0x1000

struct VRSepMboxState {
    SysBusDevice parent_obj;
    MemoryRegion mmio;
    qemu_irq irq[2];
    uint32_t regs[MBOX_SIZE / 4];
};

/* SEP message = { u8 ep; u8 tag; u8 op; u8 param; u32 data } packed into 64 bits. */
#define MSG_EP(w)    ((w) & 0xff)
#define MSG_TAG(w)   (((w) >> 8) & 0xff)
#define MSG_OP(w)    (((w) >> 16) & 0xff)
#define MSG_MK(ep, tag, op, param, data) \
    ((uint64_t)(ep) | ((uint64_t)(tag) << 8) | ((uint64_t)(op) << 16) | \
     ((uint64_t)(param) << 24) | ((uint64_t)(uint32_t)(data) << 32))

/* MMIO register offsets (reversed from AVPBooter.vresearch1.bin — see re/SEP_MAILBOX.md) */
#define R_IOP_CTRL   0x10   /* AP->SEP: 0x14 status bit31 = ready handshake */
#define R_IOP_STAT   0x14
#define R_IOP_MSG    0x18   /* handshake sentinel 0x1111 */
#define R_IN_STAT    0x1c   /* SEP->AP response status: bit16 set = not ready, 0xC0000 = error */
#define R_IN_STAT2   0x20
#define R_IN_MSG     0x100  /* SEP->AP response payload (16 bytes) */
#define R_OUT_MSG    0x200  /* AP->SEP request message word */

#define IN_NOT_READY 0x10000

static void sep_set_response(VRSepMboxState *s, uint64_t word, uint64_t extra)
{
    s->regs[R_IN_MSG / 4]     = word;
    s->regs[R_IN_MSG / 4 + 1] = word >> 32;
    s->regs[R_IN_MSG / 4 + 2] = extra;
    s->regs[R_IN_MSG / 4 + 3] = extra >> 32;
    s->regs[R_IN_STAT / 4]    = 0;          /* ready, no error */
    s->regs[R_IN_STAT2 / 4]   = 0;
    /* Signal SEP->AP: assert both IRQ lines (level-sensitive SPIs).
     * GIC SPIs are level-triggered, so we hold the line asserted until
     * the AP/XNU reads the response from R_IN_MSG or acknowledges R_IN_STAT. */
    qemu_set_irq(s->irq[0], 1);
    qemu_set_irq(s->irq[1], 1);
}

/* Handle one AP->SEP request word; produce a BOOTSTRAP/control response. */
static void sep_handle_request(VRSepMboxState *s, uint64_t req)
{
    uint8_t ep = MSG_EP(req), tag = MSG_TAG(req), op = MSG_OP(req);
    uint64_t resp;

    switch (ep) {
    case 0xff: /* EP_BOOTSTRAP: reply op = req op + 100 (PING->101, NONCE->103, ...) */
        /*
         * GENERATE_NONCE (op 3): the AP driver (AVPBooter FUN_00106be4) reads the
         * response's data32 field (resp[4:8], _DAT_7002abd4) and requires it to be
         * 0xa0 before it proceeds to read the 20-byte nonce (op 4). A zero here made
         * it skip the nonce read and firebloom-panic -> PSCI_SYSTEM_RESET.
         */
        {
            uint32_t data = 0;
            if (op == 3) {
                data = 0xa0;               /* GENERATE_NONCE status the AP checks for */
            } else if (op == 4) {
                /*
                 * READ_NONCE (op 4): the AP pulls the 20-byte nonce 4 bytes at a
                 * time (5 transactions) from the response data32 and requires the
                 * OR of all 20 bytes to be non-zero. Hand back a non-zero chunk;
                 * vary it by tag so the nonce isn't a constant run.
                 */
                data = 0xA5A50000u | tag;
            } else if (op == 2) {
                /*
                 * GET_STATUS (op 2): SEP initialization and endpoint readiness flag.
                 * Hand back ready/unlocked status bitmask so XNU endpoint poll does not hang.
                 */
                data = 0x00000001u;
            } else if (op == 16) {
                /*
                 * OP 16 (0x10): AVPBooter FUN_00103788 calls op 16 twice to read
                 * a 64-bit status/cookie (lower 32-bit then upper 32-bit).
                 * If the combined 64-bit value is zero, it panics at 0x10380c.
                 */
                data = 0x10000 | (tag ? tag : 1);
            } else if (op == 30) {
                /*
                 * KCV_INIT (op 30 / 0x1e): XNU AppleSEPBooter::_captureiBICKCV handshake.
                 * Expects ACK response op 130 (0x82) with success status.
                 */
                data = 0x00000000u;
            } else if (op == 31) {
                /*
                 * KCV_READ (op 31 / 0x1f): 8x read loop in _captureiBICKCV.
                 * Expects response op 131 (0x83) containing valid non-zero KCV key data.
                 */
                data = 0x5A5A0000u | ((uint32_t)tag << 8) | 0x01;
            }
            resp = MSG_MK(ep, tag, op + 100, 0, data);
        }
        break;
    case 0x00: /* EP_CONTROL: ACK */
        resp = MSG_MK(ep, tag, 1 /* CONTROL_OP_ACK */, 0, 0);
        break;
    default:   /* generic ACK-style echo */
        resp = MSG_MK(ep, tag, op + 100, 0, 0);
        break;
    }
    qemu_log_mask(LOG_UNIMP,
        "sep-mbox: req ep=%#x tag=%#x op=%u -> resp op=%u\n",
        ep, tag, op, MSG_OP(resp));
    sep_set_response(s, resp, 0);
}

static uint64_t mbox_read(void *opaque, hwaddr off, unsigned size)
{
    VRSepMboxState *s = opaque;
    uint64_t v = s->regs[off / 4];

    if (size == 8) {
        v |= (uint64_t)s->regs[off / 4 + 1] << 32;
    }
    qemu_log_mask(LOG_UNIMP, "sep-mbox: read  %#05" HWADDR_PRIx " -> %#" PRIx64 "\n", off, v);
    if (off == R_IN_MSG || off == R_IN_STAT) {
        /* Response consumed: lower IRQ lines */
        qemu_set_irq(s->irq[0], 0);
        qemu_set_irq(s->irq[1], 0);
    }
    (void)dump_ram; (void)diff_ram;
    return v;
}

static void mbox_write(void *opaque, hwaddr off, uint64_t v, unsigned size)
{
    VRSepMboxState *s = opaque;

    qemu_log_mask(LOG_UNIMP, "sep-mbox: write %#05" HWADDR_PRIx " <- %#" PRIx64 "\n", off, v);
    s->regs[off / 4] = v;
    if (size == 8) {
        s->regs[off / 4 + 1] = v >> 32;
    }
    /* AP acknowledged response or cleared status */
    if (off == R_IN_STAT || off == R_IOP_CTRL) {
        qemu_set_irq(s->irq[0], 0);
        qemu_set_irq(s->irq[1], 0);
    }
    /* AP wrote a request message word to the outbox -> answer it. */
    if (off == R_OUT_MSG) {
        uint64_t req = s->regs[R_OUT_MSG / 4] |
                       ((uint64_t)s->regs[R_OUT_MSG / 4 + 1] << 32);
        sep_handle_request(s, req);
    }
}

static const MemoryRegionOps mbox_ops = {
    .read = mbox_read,
    .write = mbox_write,
    .endianness = DEVICE_LITTLE_ENDIAN,
    .valid = { .min_access_size = 4, .max_access_size = 8 },
    .impl = { .min_access_size = 4, .max_access_size = 8 },
};

static void mbox_init(Object *obj)
{
    VRSepMboxState *s = VR_SEP_MBOX(obj);

    memory_region_init_io(&s->mmio, obj, &mbox_ops, s, "sep-mbox", MBOX_SIZE);
    sysbus_init_mmio(SYS_BUS_DEVICE(obj), &s->mmio);
    sysbus_init_irq(SYS_BUS_DEVICE(obj), &s->irq[0]);
    sysbus_init_irq(SYS_BUS_DEVICE(obj), &s->irq[1]);
}

static void mbox_reset(DeviceState *dev)
{
    VRSepMboxState *s = VR_SEP_MBOX(dev);

    memset(s->regs, 0, sizeof(s->regs));
}

static void mbox_class_init(ObjectClass *klass, const void *data)
{
    device_class_set_legacy_reset(DEVICE_CLASS(klass), mbox_reset);
}

static const TypeInfo mbox_info = {
    .name = TYPE_VR_SEP_MBOX,
    .parent = TYPE_SYS_BUS_DEVICE,
    .instance_size = sizeof(VRSepMboxState),
    .instance_init = mbox_init,
    .class_init = mbox_class_init,
};

static void mbox_register(void)
{
    type_register_static(&mbox_info);
}
type_init(mbox_register);
