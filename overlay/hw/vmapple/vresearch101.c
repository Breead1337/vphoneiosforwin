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
#include "hw/arm/apple-silicon/a13_gxf.h"
#include "net/net.h"
#include "qapi/error.h"
#include "qobject/qlist.h"
#include "cpu.h"
#include "target/arm/cpregs.h"
#include "exec/cputlb.h"
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
    [VR_CONFIG] =     { 0x00400000, 0x00200000 },
    [VR_PMUSRAM] =    { 0x00600000, 0x00020000 },
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

    GError *err = NULL;
    gsize len = 0;
    g_autofree char *contents = NULL;
    if (!g_file_get_contents(fname, &contents, &len, &err)) {
        error_report("vresearch101: cannot read ROM '%s': %s", fname, err->message);
        exit(1);
    }
    if (len > memmap[VR_FIRMWARE].size) {
        error_report("vresearch101: ROM '%s' is too big (%zu > %" PRIu64 ")", fname, len, (uint64_t)memmap[VR_FIRMWARE].size);
        exit(1);
    }
    uint8_t *rom = memory_region_get_ram_ptr(&vms->fw_mr);
    memcpy(rom, contents, len);

    /*
     * Bypass IM4M manifest & signature enforcement in AVPBooter:
     * At 0x101640: tbz w8, #0, 0x1016f4 (0x360005a8)
     * Replacing with: b 0x101850 (0x14000084)
     * This skips the online TSS IM4M certificate & digest validation
     * and jumps directly to IM4P payload extraction and LZFSE decompression,
     * allowing local firmware stages (LLB) to be verified and executed.
     */
    uint32_t *p_insn = (uint32_t *)(rom + (0x101640 - 0x100000));
    fprintf(stderr, "vresearch101: loaded ROM '%s' (%zu bytes), insn @ 0x101640 = 0x%08x\n", fname, len, *p_insn);
    if (*p_insn == 0x360005a8) {
        fprintf(stderr, "vresearch101: patching AVPBooter IM4M check at 0x101640 -> b 0x101850 (0x14000084)\n");
        *p_insn = 0x14000084;
    }

    memory_region_add_subregion(get_system_memory(), memmap[VR_FIRMWARE].base,
                                &vms->fw_mr);
}

static void vr_reset(void *opaque)
{
    cpu_set_pc(first_cpu, memmap[VR_FIRMWARE].base);
}

/*
 * Apple implementation sysregs used by SPTM/TXM/kernel of vresearch101 (census: MRS/MSR with CRn 11/15 in the
 * images) that the apple-gxf CPU lacks. The rest read as zero, writes ignored.
 * ponytail: RAZ/WI stubs; give a register real storage once a guest reads back what it wrote.
 */
static void vr_cpreg_stub(ARMCPU *cpu, uint8_t op1, uint8_t crn, uint8_t crm, uint8_t op2, uint64_t val)
{
    uint32_t key = ENCODE_AA64_CP_REG(CP_REG_ARM64_SYSREG_CP, crn, crm, 3, op1, op2);
    ARMCPRegInfo r = {
        .name = g_strdup_printf("VR_S3_%u_C%u_C%u_%u", op1, crn, crm, op2),
        .state = ARM_CP_STATE_AA64, .opc0 = 3, .opc1 = op1, .crn = crn, .crm = crm, .opc2 = op2,
        .access = PL1_RW, .type = ARM_CP_CONST, .resetvalue = val,
    };

    if (!ARMCPRegTable_cget(cpu->cp_regs, key)) {
        define_one_arm_cp_reg(cpu, &r);
    }
}

static void vr_sprr_perm_write(CPUARMState *env, const ARMCPRegInfo *ri, uint64_t value)
{
    raw_write(env, ri, value);
    tlb_flush(env_cpu(env));
}

/*
 * SPRR layout of this core generation (SPTM: msr S3_6_C15_C1_6 = EL1 perms, then reads it back and hangs on
 * mismatch; C1_5 = EL0 perms): Inferno's A13 walker takes EL1 perms from sprr_el_br_el1[1][1] (its C3_0), so point
 * C1_6 there and park C3_0 (only a get/set accessor pair in SPTM) on the otherwise unused [1][0].
 */
static const ARMCPRegInfo vr_sprr_override_reginfo[] = {
    { .name = "SPRR_PERM_EL1", .state = ARM_CP_STATE_AA64,
      .opc0 = 3, .opc1 = 6, .crn = 15, .crm = 1, .opc2 = 6,
      .access = PL1_RW, .type = ARM_CP_OVERRIDE,
      .readfn = raw_read, .writefn = vr_sprr_perm_write, .raw_writefn = raw_write,
      .fieldoffset = offsetof(CPUARMState, sprr.sprr_el_br_el1[1][1]) },
    { .name = "SPRR_S3_6_C15_C3_0", .state = ARM_CP_STATE_AA64,
      .opc0 = 3, .opc1 = 6, .crn = 15, .crm = 3, .opc2 = 0,
      .access = PL1_RW, .type = ARM_CP_OVERRIDE,
      .readfn = raw_read, .writefn = raw_write,
      .fieldoffset = offsetof(CPUARMState, sprr.sprr_el_br_el1[1][0]) },
};

#define VR_GL1_REG(nm, op2, field) { .name = nm, .state = ARM_CP_STATE_AA64, .opc0 = 3, .opc1 = 6, .crn = 15, .crm = 10, .opc2 = op2, .access = PL1_RW, .fieldoffset = offsetof(CPUARMState, gxf.field[1]) }

/* GL1 banked registers of this core generation live at S3_6_C15_C10_x (A13 model: C9_x) */
static const ARMCPRegInfo vr_gl1_reginfo[] = {
    VR_GL1_REG("SP_GL1", 0, sp_gl),       VR_GL1_REG("TPIDR_GL1", 1, tpidr_gl),
    VR_GL1_REG("VBAR_GL1", 2, vbar_gl),   VR_GL1_REG("SPSR_GL1", 3, spsr_gl),
    VR_GL1_REG("ASPSR_GL1", 4, aspsr_gl), VR_GL1_REG("ESR_GL1", 5, esr_gl),
    VR_GL1_REG("ELR_GL1", 6, elr_gl),     VR_GL1_REG("FAR_GL1", 7, far_gl),
};

static void vr_apple_cpregs(ARMCPU *cpu)
{
    define_arm_cp_regs(cpu, vr_gl1_reginfo);
    define_arm_cp_regs(cpu, vr_sprr_override_reginfo);
    vr_cpreg_stub(cpu, 6, 15, 12, 4, 1); /* APSTS_EL1: MKeyVld (Inferno only has it in APCTL) */
    vr_cpreg_stub(cpu, 0, 15, 4, 0, 0);  /* HID4 */
    vr_cpreg_stub(cpu, 1, 11, 8, 1, 0);
    vr_cpreg_stub(cpu, 3, 15, 0, 0, 0);
    vr_cpreg_stub(cpu, 3, 15, 8, 0, 0);  /* LLC_ERR_STS */
    vr_cpreg_stub(cpu, 3, 15, 9, 0, 0);  /* LLC_ERR_ADR */
    vr_cpreg_stub(cpu, 3, 15, 10, 0, 0); /* LLC_ERR_INF */
    vr_cpreg_stub(cpu, 4, 15, 0, 0, 0);
    for (uint8_t op2 = 0; op2 < 4; op2++) {
        vr_cpreg_stub(cpu, 4, 15, 10, op2, 0);
    }
    vr_cpreg_stub(cpu, 5, 15, 2, 6, 0);
    vr_cpreg_stub(cpu, 5, 15, 5, 0, 0);  /* CPU_OVRD */
    vr_cpreg_stub(cpu, 6, 15, 0, 0, 0);
    vr_cpreg_stub(cpu, 6, 15, 0, 2, 0);
    vr_cpreg_stub(cpu, 6, 15, 1, 3, 0);
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
        /*
         * SPTM runs in GXF and programs SPRR/GXF sysregs (first: S3_6_C15_C1_0 SPRR_CONFIG_EL1).
         * Inferno defines them only for its A13 CPU; they touch nothing but the ARMCPU parent
         * (first member of AppleA13State), so register the same sets on our apple-gxf CPU.
         */
        apple_a13_init_gxf((AppleA13State *)cpu);
        qdev_realize(DEVICE(cpu), NULL, &error_fatal);
        apple_a13_init_gxf_override((AppleA13State *)cpu);
        vr_apple_cpregs(ARM_CPU(cpu));
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
