import capstone

md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)

f = open('/mnt/d/vphonewin/fw/cloud/raw/dyld.bin', 'rb')

targets = [
    (0x700e0708, 0xe0708, "imm=197 (0xc5)"),
    (0x70082410, 0x82410, "imm=0"),
    (0x70082418, 0x82418, "imm=1"),
    (0x700dc75c, 0xdc75c, "imm=66 (0x42)"),
    (0x700e0668, 0xe0668, "imm=98 (0x62)"),
    (0x70082400, 0x82400, "imm=50 (0x32)"),
    (0x700c2d50, 0xc2d50, "imm=195 (0xc3)"),
    (0x700c2db4, 0xc2db4, "imm=196 (0xc4)"),
    (0x7009b780, 0x9b780, "imm=194 (0xc2)"),
    (0x70088998, 0x88998, "imm=58 (0x3a)"),
    (0x7008893c, 0x8893c, "imm=101 (0x65)")
]

for vm, off, desc in targets:
    f.seek(off - 20)
    code = f.read(40)
    print(f"\n=======================================================")
    print(f"Target {vm:#x} (file offset {off:#x}) - {desc}:")
    for ins in md.disasm(code, vm - 20):
        mark = "==> " if ins.address == vm else "    "
        print(f"{mark}{ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")
