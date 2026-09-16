/*
 * VMApple Backdoor Interface
 *
 * Copyright © 2023 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * This work is licensed under the terms of the GNU GPL, version 2 or later.
 * See the COPYING file in the top-level directory.
 *
 * SPDX-License-Identifier: GPL-2.0-or-later
 */

#include "qemu/osdep.h"
#include "qemu/units.h"
#include "qemu/log.h"
#include "qemu/module.h"
#include "trace.h"
#include "hw/vmapple/vmapple.h"
#include "hw/sysbus.h"
#include "hw/block/block.h"
#include "qapi/error.h"
#include "system/block-backend.h"
#include "system/dma.h"

OBJECT_DECLARE_SIMPLE_TYPE(VMAppleBdifState, VMAPPLE_BDIF)

struct VMAppleBdifState {
    SysBusDevice parent_obj;

    BlockBackend *aux;
    BlockBackend *root;
    MemoryRegion mmio;
};

#define VMAPPLE_BDIF_SIZE   0x00200000

#define REG_DEVID_MASK      0xffff0000
#define DEVID_ROOT          0x00000000
#define DEVID_AUX           0x00010000
#define DEVID_USB           0x00100000

#define REG_STATUS          0x0
#define REG_STATUS_ACTIVE     BIT(0)
#define REG_CFG             0x4
#define REG_CFG_ACTIVE        BIT(1)
#define REG_UNK1            0x8
#define REG_BUSY            0x10
#define REG_BUSY_READY        BIT(0)
#define REG_UNK2            0x400
#define REG_CMD             0x408
#define REG_NEXT_DEVICE     0x420
#define REG_UNK3            0x434

typedef struct VblkSector {
    uint32_t pad;
    uint32_t pad2;
    uint32_t sector;
    uint32_t pad3;
} VblkSector;

typedef struct VblkReqCmd {
    uint64_t addr;
    uint32_t len;
    uint32_t flags;
} VblkReqCmd;

typedef struct VblkReq {
    VblkReqCmd sector;
    VblkReqCmd data;
    VblkReqCmd retval;
} VblkReq;

#define VBLK_DATA_FLAGS_READ  0x00030001
#define VBLK_DATA_FLAGS_WRITE 0x00010001

#define VBLK_RET_SUCCESS  0
#define VBLK_RET_FAILED   1

static uint64_t bdif_read(void *opaque, hwaddr offset, unsigned size)
{
    uint64_t ret = -1;
    uint64_t devid = offset & REG_DEVID_MASK;

    switch (offset & ~REG_DEVID_MASK) {
    case REG_STATUS:
        ret = REG_STATUS_ACTIVE;
        break;
    case REG_CFG:
        if (devid == DEVID_USB) {
            ret = 0x1a01;
        } else {
            ret = REG_CFG_ACTIVE;
        }
        break;
    case REG_UNK1:
        ret = 0x420;
        break;
    case REG_BUSY:
        if (devid == DEVID_USB) {
            ret = 0;
        } else {
            ret = REG_BUSY_READY;
        }
        break;
    case REG_UNK2:
        ret = 0x1;
        break;
    case REG_UNK3:
        ret = 0x0;
        break;
    case REG_NEXT_DEVICE:
        switch (devid) {
        case DEVID_ROOT:
            ret = 0x8000000;
            break;
        case DEVID_AUX:
            ret = 0x10000;
            break;
        }
        break;
    }

    qemu_log_mask(LOG_UNIMP, "bdif_read: devid=%#" PRIx64 " off=%#" HWADDR_PRIx " -> %#" PRIx64 "\n", devid, offset & ~REG_DEVID_MASK, ret);
    trace_bdif_read(offset, size, ret);
    return ret;
}

static void le2cpu_sector(VblkSector *sector)
{
    sector->sector = le32_to_cpu(sector->sector);
}

static void le2cpu_reqcmd(VblkReqCmd *cmd)
{
    cmd->addr = le64_to_cpu(cmd->addr);
    cmd->len = le32_to_cpu(cmd->len);
    cmd->flags = le32_to_cpu(cmd->flags);
}

static void le2cpu_req(VblkReq *req)
{
    le2cpu_reqcmd(&req->sector);
    le2cpu_reqcmd(&req->data);
    le2cpu_reqcmd(&req->retval);
}

static void vblk_cmd(uint64_t devid, BlockBackend *blk, uint64_t gp_addr,
                     uint64_t static_off)
{
    VblkReq req;
    VblkSector sector;
    uint64_t off = 0;
    g_autofree char *buf = NULL;
    uint8_t ret = VBLK_RET_FAILED;
    int r;
    MemTxResult dma_result;

    if (!blk) {
        goto out;
    }
    dma_result = dma_memory_read(&address_space_memory, gp_addr,
                                 &req, sizeof(req), MEMTXATTRS_UNSPECIFIED);
    if (dma_result != MEMTX_OK) {
        goto out;
    }

    le2cpu_req(&req);

    if (req.sector.len != sizeof(sector)) {
        goto out;
    }

    /* Read the vblk command */
    dma_result = dma_memory_read(&address_space_memory, req.sector.addr,
                                 &sector, sizeof(sector),
                                 MEMTXATTRS_UNSPECIFIED);
    if (dma_result != MEMTX_OK) {
        goto out;
    }
    le2cpu_sector(&sector);

    off = sector.sector * 512ULL + static_off;

    /* Sanity check that we're not allocating bogus sizes */
    if (req.data.len > 128 * MiB) {
        goto out;
    }

    buf = g_malloc0(req.data.len);
    switch (req.data.flags) {
    case VBLK_DATA_FLAGS_READ:
        r = blk_pread(blk, off, req.data.len, buf, 0);
        qemu_log_mask(LOG_UNIMP, "bdif vblk_read: %s addr=%#" PRIx64 " off=%#" PRIx64 " len=%u r=%d\n",
                      devid == DEVID_AUX ? "aux" : "root", req.data.addr, off, req.data.len, r);
        trace_bdif_vblk_read(devid == DEVID_AUX ? "aux" : "root",
                             req.data.addr, off, req.data.len, r);
        if (r < 0) {
            goto out;
        }
        dma_result = dma_memory_write(&address_space_memory, req.data.addr, buf,
                                      req.data.len, MEMTXATTRS_UNSPECIFIED);
        if (dma_result == MEMTX_OK) {
            ret = VBLK_RET_SUCCESS;
        }
        break;
    case VBLK_DATA_FLAGS_WRITE:
        dma_result = dma_memory_read(&address_space_memory, req.data.addr, buf,
                                     req.data.len, MEMTXATTRS_UNSPECIFIED);
        if (dma_result != MEMTX_OK) {
            goto out;
        }
        r = blk_pwrite(blk, off, req.data.len, buf, 0);
        qemu_log_mask(LOG_UNIMP, "bdif vblk_write: %s addr=%#" PRIx64 " off=%#" PRIx64 " len=%u r=%d\n",
                      devid == DEVID_AUX ? "aux" : "root", req.data.addr, off, req.data.len, r);
        if (r >= 0) {
            ret = VBLK_RET_SUCCESS;
        }
        break;
    default:
        qemu_log_mask(LOG_UNIMP, "bdif vblk unknown flags=%#x\n", req.data.flags);
        break;
    }

out:
    dma_memory_write(&address_space_memory, req.retval.addr, &ret, 1,
                     MEMTXATTRS_UNSPECIFIED);
}

static void bdif_write(void *opaque, hwaddr offset,
                       uint64_t value, unsigned size)
{
    VMAppleBdifState *s = opaque;
    uint64_t devid = (offset & REG_DEVID_MASK);

    qemu_log_mask(LOG_UNIMP, "bdif_write: devid=%#" PRIx64 " off=%#" HWADDR_PRIx " val=%#" PRIx64 "\n", devid, offset & ~REG_DEVID_MASK, value);
    trace_bdif_write(offset, size, value);

    switch (offset & ~REG_DEVID_MASK) {
    case REG_CMD:
        switch (devid) {
        case DEVID_ROOT:
            vblk_cmd(devid, s->root, value, 0x0);
            break;
        case DEVID_AUX:
            vblk_cmd(devid, s->aux, value, 0x0);
            break;
        case DEVID_USB: {
            uint8_t d[0x80];
            if (dma_memory_read(&address_space_memory, value, d, sizeof(d), MEMTXATTRS_UNSPECIFIED) == MEMTX_OK) {
                char hex[3 * 16 + 1];
                qemu_log_mask(LOG_UNIMP, "bdif DEVID_USB cmd @%#" PRIx64 ":\n", value);
                for (int i = 0; i < 0x20; i += 16) {
                    int p = 0;
                    for (int j = 0; j < 16; j++) {
                        p += snprintf(hex + p, sizeof(hex) - p, "%02x ", d[i + j]);
                    }
                    qemu_log_mask(LOG_UNIMP, "  %#04x: %s\n", i, hex);
                }
                uint64_t sub_addr = ldq_le_p(d);
                uint8_t buf[0x80];
                if (dma_memory_read(&address_space_memory, sub_addr, buf, sizeof(buf), MEMTXATTRS_UNSPECIFIED) == MEMTX_OK) {
                    qemu_log_mask(LOG_UNIMP, "  -> buffer @%#" PRIx64 ":\n", sub_addr);
                    for (int i = 0; i < sizeof(buf); i += 16) {
                        int p = 0;
                        for (int j = 0; j < 16; j++) {
                            p += snprintf(hex + p, sizeof(hex) - p, "%02x ", buf[i + j]);
                        }
                        qemu_log_mask(LOG_UNIMP, "    %#04x: %s\n", i, hex);
                    }
                }
            }
            break;
        }
        }
        break;
    }
}

static const MemoryRegionOps bdif_ops = {
    .read = bdif_read,
    .write = bdif_write,
    .endianness = DEVICE_NATIVE_ENDIAN,
    .valid = {
        .min_access_size = 1,
        .max_access_size = 8,
    },
    .impl = {
        .min_access_size = 1,
        .max_access_size = 8,
    },
};

static void bdif_init(Object *obj)
{
    VMAppleBdifState *s = VMAPPLE_BDIF(obj);

    memory_region_init_io(&s->mmio, obj, &bdif_ops, obj,
                         "VMApple Backdoor Interface", VMAPPLE_BDIF_SIZE);
    sysbus_init_mmio(SYS_BUS_DEVICE(obj), &s->mmio);
}

static const Property bdif_properties[] = {
    DEFINE_PROP_DRIVE("aux", VMAppleBdifState, aux),
    DEFINE_PROP_DRIVE("root", VMAppleBdifState, root),
};

static void bdif_realize(DeviceState *dev, Error **errp)
{
    VMAppleBdifState *s = VMAPPLE_BDIF(dev);

    if (s->aux) {
        if (blk_set_perm(s->aux, BLK_PERM_CONSISTENT_READ | BLK_PERM_WRITE,
                         BLK_PERM_ALL, errp) < 0) {
            return;
        }
    }
    if (s->root) {
        if (blk_set_perm(s->root, BLK_PERM_CONSISTENT_READ | BLK_PERM_WRITE,
                         BLK_PERM_ALL, errp) < 0) {
            return;
        }
    }
}

static void bdif_class_init(ObjectClass *klass, const void *data)
{
    DeviceClass *dc = DEVICE_CLASS(klass);

    dc->realize = bdif_realize;
    dc->desc = "VMApple Backdoor Interface";
    device_class_set_props(dc, bdif_properties);
}

static const TypeInfo bdif_info = {
    .name          = TYPE_VMAPPLE_BDIF,
    .parent        = TYPE_SYS_BUS_DEVICE,
    .instance_size = sizeof(VMAppleBdifState),
    .instance_init = bdif_init,
    .class_init    = bdif_class_init,
};

static void bdif_register_types(void)
{
    type_register_static(&bdif_info);
}

type_init(bdif_register_types)
