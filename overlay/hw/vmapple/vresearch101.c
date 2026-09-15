/*
 * vresearch101 machine: the "PCC Research Environment" / vphone platform that
 * Apple's Virtualization.framework exposes (AVPBooter.vresearch1.bin).
 *
 * Same MMIO layout as vmapple (arm-io at 0x10000000), plus a SEP mailbox,
 * AVP RTC and AVP CTRR block. Runs on TCG with Inferno's GXF/SPRR CPU so it
 * works on x86 hosts.
 *
 * SPDX-License-Identifier: GPL-2.0-or-later
 */

#include "qemu/osdep.h"
#include "qemu/datadir.h"
#include "qemu/error-report.h"
#include "qemu/guest-random.h"
#include "qemu/log.h"
#include "qemu/units.h"
#include "hw/boards.h"
#include "hw/irq.h"
#include "hw/loader.h"
#include "hw/qdev-properties.h"
#include "hw/sysbus.h"
#include "hw/usb.h"
#include "hw/arm/boot.h"
#include "hw/char/pl011.h"
#include "hw/intc/arm_gicv3_common.h"
#include "hw/misc/pvpanic.h"
#include "hw/misc/unimp.h"
#include "hw/pci-host/gpex.h"
#include "hw/usb/hcd-xhci-pci.h"
#include "hw/virtio/virtio-pci.h"
#include "hw/vmapple/vmapple.h"
#include "net/net.h"
#include "qapi/error.h"
#include "qobject/qlist.h"
#include "cpu.h"
#include "system/reset.h"
#include "system/runstate.h"
#include "system/system.h"
#include "system/block-backend.h"

struct VResearchMachineState {
    MachineState parent;

    DeviceState *gic;
    DeviceState *cfg;
    PCIBus *bus;
    MemoryRegion fw_mr;
    MemoryRegion pmusram;
    MemoryRegion ecam_alias;
    uint64_t ecid;
    Notifier powerdown_notifier;
};

#define TYPE_VRESEARCH_MACHINE MACHINE_TYPE_NAME("vresearch101")
OBJECT_DECLARE_SIMPLE_TYPE(VResearchMachineState, VRESEARCH_MACHINE)

#define NUM_IRQS 256
#define GPEX_NUM_IRQS 16

enum {
    VR_FIRMWARE, VR_CONFIG, VR_PMUSRAM, VR_MEM, VR_GIC_DIST, VR_GIC_REDIST, VR_UART,
    VR_RTC, VR_GPIO, VR_PVPANIC, VR_BDOOR, VR_APV_GFX, VR_APV_IOSFC,
    VR_AES_1, VR_AES_2, VR_AVP_RTC, VR_SEP, VR_AVP_CTRR, VR_PCIE,
    VR_PCIE_ECAM, VR_PCIE_MMIO,
};

/* From DeviceTree.vresearch101ap: arm-io child 0 -> parent 0x10000000 */
static const MemMapEntry memmap[] = {
    [VR_FIRMWARE] =   { 0x00100000, 0x00100000 },
    [VR_CONFIG] =     { 0x00400000, 0x00010000 },
    [VR_PMUSRAM] =    { 0x00600000, 0x00010000 },
    [VR_GIC_DIST] =   { 0x10000000, 0x00010000 },
    [VR_GIC_REDIST] = { 0x10010000, 0x00400000 },
    [VR_UART] =       { 0x20010000, 0x00010000 },
    [VR_RTC] =        { 0x20050000, 0x00001000 },
    [VR_GPIO] =       { 0x20060000, 0x00001000 },
    [VR_PVPANIC] =    { 0x20070000, 0x00000002 },
    [VR_BDOOR] =      { 0x30000000, 0x00200000 },
    [VR_APV_GFX] =    { 0x30200000, 0x00010000 },
    [VR_APV_IOSFC] =  { 0x30210000, 0x00010000 },
    [VR_AES_1] =      { 0x30220000, 0x00004000 },
    [VR_AES_2] =      { 0x30230000, 0x00004000 },
    [VR_AVP_RTC] =    { 0x30240000, 0x00001000 },
    [VR_SEP] =        { 0x30250000, 0x00001000 },
    [VR_AVP_CTRR] =   { 0x30260000, 0x00010000 },
    [VR_PCIE_ECAM] =  { 0x40000000, 0x10000000 },
    [VR_PCIE_MMIO] =  { 0x50000000, 0x1fff0000 },
    [VR_MEM] =        { 0x70000000ULL, GiB },
};

/* SPI numbers; DT "interrupts" = SPI + 32 */
static const int irqmap[] = {
    [VR_UART] = 1, [VR_RTC] = 2, [VR_GPIO] = 5,
    [VR_APV_IOSFC] = 0x10, [VR_APV_GFX] = 0x11, [VR_AES_1] = 0x12,
    [VR_AVP_RTC] = 0x13, [VR_SEP] = 0x14, [VR_PCIE] = 0x20,
};

static void create_gic(VResearchMachineState *vms)
{
    MachineState *ms = MACHINE(vms);
    unsigned int n = ms->smp.cpus;
    QList *rc = qlist_new();
    SysBusDevice *sbd;

    vms->gic = qdev_new(gicv3_class_name());
    qdev_prop_set_uint32(vms->gic, "revision", 3);
    qdev_prop_set_uint32(vms->gic, "num-cpu", n);
    qdev_prop_set_uint32(vms->gic, "num-irq", NUM_IRQS + 32);
    qlist_append_int(rc, MIN(n, memmap[VR_GIC_REDIST].size / GICV3_REDIST_SIZE));
    qdev_prop_set_array(vms->gic, "redist-region-count", rc);
    sbd = SYS_BUS_DEVICE(vms->gic);
    sysbus_realize_and_unref(sbd, &error_fatal);
    sysbus_mmio_map(sbd, 0, memmap[VR_GIC_DIST].base);
    sysbus_mmio_map(sbd, 1, memmap[VR_GIC_REDIST].base);

    for (unsigned int i = 0; i < n; i++) {
        DeviceState *cpu = DEVICE(qemu_get_cpu(i));
        int ppi = NUM_IRQS + i * GIC_INTERNAL;
        qdev_connect_gpio_out(cpu, GTIMER_VIRT, qdev_get_gpio_in(vms->gic, ppi + 27));
        qdev_connect_gpio_out(cpu, GTIMER_PHYS, qdev_get_gpio_in(vms->gic, ppi + 30));
        sysbus_connect_irq(sbd, i, qdev_get_gpio_in(cpu, ARM_CPU_IRQ));
        sysbus_connect_irq(sbd, i + n, qdev_get_gpio_in(cpu, ARM_CPU_FIQ));
    }
}

static qemu_irq spi(VResearchMachineState *vms, int dev)
{
    return qdev_get_gpio_in(vms->gic, irqmap[dev]);
}

static void create_bdif(VResearchMachineState *vms)
{
    DriveInfo *aux = drive_get(IF_PFLASH, 0, 0);
    DriveInfo *root = drive_get(IF_PFLASH, 0, 1);
    DeviceState *dev = qdev_new(TYPE_VMAPPLE_BDIF);

    if (!root) {
        root = drive_get(IF_VIRTIO, 0, 0);
    }
    if (aux) {
        qdev_prop_set_drive(dev, "aux", blk_by_legacy_dinfo(aux));
    }
    if (root) {
        qdev_prop_set_drive(dev, "root", blk_by_legacy_dinfo(root));
    }
    sysbus_realize_and_unref(SYS_BUS_DEVICE(dev), &error_fatal);
    sysbus_mmio_map(SYS_BUS_DEVICE(dev), 0, memmap[VR_BDOOR].base);
}

static void create_cfg(VResearchMachineState *vms)
{
    MachineState *ms = MACHINE(vms);
    uint32_t rnd = 1;

    vms->cfg = qdev_new(TYPE_VMAPPLE_CFG);
    qemu_guest_getrandom_nofail(&rnd, sizeof(rnd));
    qdev_prop_set_uint32(vms->cfg, "nr-cpus", ms->smp.cpus);
    qdev_prop_set_uint64(vms->cfg, "ecid", vms->ecid);
    qdev_prop_set_uint64(vms->cfg, "ram-size", ms->ram_size);
    qdev_prop_set_uint32(vms->cfg, "rnd", rnd);
    qdev_prop_set_string(vms->cfg, "soc_name", "Apple VResearch1 (Virtual)");
    sysbus_realize_and_unref(SYS_BUS_DEVICE(vms->cfg), &error_fatal);
    sysbus_mmio_map(SYS_BUS_DEVICE(vms->cfg), 0, memmap[VR_CONFIG].base);
}

static void create_pcie(VResearchMachineState *vms)
{
    DeviceState *dev = qdev_new(TYPE_GPEX_HOST);
    MemoryRegion *mmio_alias = g_new0(MemoryRegion, 1);
    PCIHostState *pci;

    qdev_prop_set_uint32(dev, "num-irqs", GPEX_NUM_IRQS);
    sysbus_realize_and_unref(SYS_BUS_DEVICE(dev), &error_fatal);
    memory_region_init_alias(&vms->ecam_alias, OBJECT(dev), "pcie-ecam",
                             sysbus_mmio_get_region(SYS_BUS_DEVICE(dev), 0),
                             0, memmap[VR_PCIE_ECAM].size);
    memory_region_add_subregion(get_system_memory(), memmap[VR_PCIE_ECAM].base,
                                &vms->ecam_alias);
    memory_region_init_alias(mmio_alias, OBJECT(dev), "pcie-mmio",
                             sysbus_mmio_get_region(SYS_BUS_DEVICE(dev), 1),
                             memmap[VR_PCIE_MMIO].base, memmap[VR_PCIE_MMIO].size);
    memory_region_add_subregion(get_system_memory(), memmap[VR_PCIE_MMIO].base,
                                mmio_alias);
    for (int i = 0; i < GPEX_NUM_IRQS; i++) {
        sysbus_connect_irq(SYS_BUS_DEVICE(dev), i,
                           qdev_get_gpio_in(vms->gic, irqmap[VR_PCIE] + i));
        gpex_set_irq_num(GPEX_HOST(dev), i, irqmap[VR_PCIE] + i);
    }
    pci = PCI_HOST_BRIDGE(dev);
    vms->bus = pci->bus;
    while ((dev = qemu_create_nic_device("virtio-net-pci", true, NULL))) {
        qdev_realize_and_unref(dev, BUS(vms->bus), &error_fatal);
    }
}

static DeviceState *gpio_key_dev;
static void vr_powerdown_req(Notifier *n, void *opaque)
{
    qemu_set_irq(qdev_get_gpio_in(gpio_key_dev, 0), 1);
}

static void create_gpio(VResearchMachineState *vms)
{
    DeviceState *pl061 = qdev_new("pl061");

    qdev_prop_set_uint32(pl061, "pullups", 0);
    qdev_prop_set_uint32(pl061, "pulldowns", 0xff);
    sysbus_realize_and_unref(SYS_BUS_DEVICE(pl061), &error_fatal);
    sysbus_mmio_map(SYS_BUS_DEVICE(pl061), 0, memmap[VR_GPIO].base);
    sysbus_connect_irq(SYS_BUS_DEVICE(pl061), 0, spi(vms, VR_GPIO));
    gpio_key_dev = sysbus_create_simple("gpio-key", -1, qdev_get_gpio_in(pl061, 3));
}

static void load_firmware(VResearchMachineState *vms)
{
    const char *name = MACHINE(vms)->firmware;
    g_autofree char *fname = NULL;

    if (!name) {
        error_report("vresearch101: pass AVPBooter.vresearch1.bin with -bios");
        exit(1);
    }
    fname = qemu_find_file(QEMU_FILE_TYPE_BIOS, name);
    if (!fname) {
        error_report("vresearch101: cannot find ROM '%s'", name);
        exit(1);
    }
    memory_region_init_ram(&vms->fw_mr, NULL, "avpbooter", memmap[VR_FIRMWARE].size,
                           &error_fatal);
    if (load_image_mr(fname, &vms->fw_mr) < 0) {
        error_report("vresearch101: cannot load ROM '%s'", fname);
        exit(1);
    }
    memory_region_add_subregion(get_system_memory(), memmap[VR_FIRMWARE].base,
                                &vms->fw_mr);
}

static void vr_reset(void *opaque)
{
    cpu_set_pc(first_cpu, memmap[VR_FIRMWARE].base);
}

static void vr_init(MachineState *machine)
{
    VResearchMachineState *vms = VRESEARCH_MACHINE(machine);
    MemoryRegion *sysmem = get_system_memory();
    SysBusDevice *sbd;

    for (unsigned int n = 0; n < machine->smp.cpus; n++) {
        Object *cpu = object_new(machine->cpu_type);

        object_property_set_int(cpu, "mp-affinity",
                                arm_build_mp_affinity(n, GICV3_TARGETLIST_BITS),
                                &error_fatal);
        if (object_property_find(cpu, "has_el3")) {
            object_property_set_bool(cpu, "has_el3", false, &error_fatal);
        }
        if (object_property_find(cpu, "has_el2")) {
            object_property_set_bool(cpu, "has_el2", false, &error_fatal);
        }
        object_property_set_int(cpu, "psci-conduit", QEMU_PSCI_CONDUIT_HVC,
                                &error_fatal);
        object_property_set_uint(cpu, "cntfrq", 24000000, &error_fatal);
        if (n > 0) {
            object_property_set_bool(cpu, "start-powered-off", true, &error_fatal);
        }
        object_property_set_link(cpu, "memory", OBJECT(sysmem), &error_abort);
        qdev_realize(DEVICE(cpu), NULL, &error_fatal);
        object_unref(cpu);
    }

    memory_region_add_subregion(sysmem, memmap[VR_MEM].base, machine->ram);

    /* PMU SRAM: boot nonce @0x90..0xd4, power request @0x400; survives reset */
    memory_region_init_ram(&vms->pmusram, NULL, "pmusram", memmap[VR_PMUSRAM].size,
                           &error_fatal);
    memory_region_add_subregion(sysmem, memmap[VR_PMUSRAM].base, &vms->pmusram);

    create_gic(vms);
    create_bdif(vms);

    vms->cfg = NULL;
    sbd = SYS_BUS_DEVICE(qdev_new(TYPE_PVPANIC_MMIO_DEVICE));
    sysbus_realize_and_unref(sbd, &error_fatal);
    sysbus_mmio_map(sbd, 0, memmap[VR_PVPANIC].base);

    sbd = SYS_BUS_DEVICE(qdev_new(TYPE_VMAPPLE_AES));
    sysbus_realize_and_unref(sbd, &error_fatal);
    sysbus_mmio_map(sbd, 0, memmap[VR_AES_1].base);
    sysbus_mmio_map(sbd, 1, memmap[VR_AES_2].base);
    sysbus_connect_irq(sbd, 0, spi(vms, VR_AES_1));

    sbd = SYS_BUS_DEVICE(qdev_new(TYPE_PL011));
    qdev_prop_set_chr(DEVICE(sbd), "chardev", serial_hd(0));
    sysbus_realize_and_unref(sbd, &error_fatal);
    sysbus_mmio_map(sbd, 0, memmap[VR_UART].base);
    sysbus_connect_irq(sbd, 0, spi(vms, VR_UART));

    sysbus_create_simple("pl031", memmap[VR_RTC].base, spi(vms, VR_RTC));

    /* ponytail: logging stubs until each block is reversed */
    create_unimplemented_device("apv-gfx", memmap[VR_APV_GFX].base, memmap[VR_APV_GFX].size);
    create_unimplemented_device("apv-iosfc", memmap[VR_APV_IOSFC].base, memmap[VR_APV_IOSFC].size);
    create_unimplemented_device("avp-rtc", memmap[VR_AVP_RTC].base, memmap[VR_AVP_RTC].size);
    sbd = SYS_BUS_DEVICE(qdev_new(TYPE_VR_SEP_MBOX));
    sysbus_realize_and_unref(sbd, &error_fatal);
    sysbus_mmio_map(sbd, 0, memmap[VR_SEP].base);
    sysbus_connect_irq(sbd, 0, qdev_get_gpio_in(vms->gic, 0x14));
    sysbus_connect_irq(sbd, 1, qdev_get_gpio_in(vms->gic, 0x15));
    create_unimplemented_device("avp-ctrr", memmap[VR_AVP_CTRR].base, memmap[VR_AVP_CTRR].size);

    create_pcie(vms);
    create_gpio(vms);
    load_firmware(vms);
    create_cfg(vms);

    vms->powerdown_notifier.notify = vr_powerdown_req;
    qemu_register_powerdown_notifier(&vms->powerdown_notifier);
    qemu_register_reset(vr_reset, vms);
}

static const CPUArchIdList *vr_possible_cpu_arch_ids(MachineState *ms)
{
    if (!ms->possible_cpus) {
        ms->possible_cpus = g_malloc0(sizeof(CPUArchIdList) +
                                      sizeof(CPUArchId) * ms->smp.max_cpus);
        ms->possible_cpus->len = ms->smp.max_cpus;
        for (unsigned int n = 0; n < ms->smp.max_cpus; n++) {
            ms->possible_cpus->cpus[n].type = ms->cpu_type;
            ms->possible_cpus->cpus[n].arch_id =
                arm_build_mp_affinity(n, GICV3_TARGETLIST_BITS);
        }
    }
    return ms->possible_cpus;
}

static void vr_class_init(ObjectClass *oc, const void *data)
{
    MachineClass *mc = MACHINE_CLASS(oc);

    mc->init = vr_init;
    mc->desc = "Apple PCC Research Environment VM (vresearch101 / vphone)";
    mc->max_cpus = 32;
    mc->block_default_type = IF_VIRTIO;
    mc->no_cdrom = 1;
    mc->pci_allow_0_address = true;
    mc->minimum_page_bits = 12;
    mc->possible_cpu_arch_ids = vr_possible_cpu_arch_ids;
    mc->default_cpu_type = ARM_CPU_TYPE_NAME("apple-gxf");
    mc->default_ram_id = "vresearch101.ram";
    mc->default_ram_size = 4 * GiB;
}

static void vr_instance_init(Object *obj)
{
    VResearchMachineState *vms = VRESEARCH_MACHINE(obj);

    object_property_add_uint64_ptr(obj, "ecid", &vms->ecid, OBJ_PROP_FLAG_READWRITE);
}

static const TypeInfo vr_info = {
    .name = TYPE_VRESEARCH_MACHINE,
    .parent = TYPE_MACHINE,
    .instance_size = sizeof(VResearchMachineState),
    .class_init = vr_class_init,
    .instance_init = vr_instance_init,
};

static void vr_register(void)
{
    type_register_static(&vr_info);
}
type_init(vr_register);
