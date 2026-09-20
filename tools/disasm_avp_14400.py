import capstone

md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)

with open('/mnt/d/vphonewin/fw/vz/AVPBooter.vresearch1.bin', 'rb') as f:
    f.seek(0x14400)
    code = f.read(64)
    print("Disassembly of AVPBooter at offset 0x14400:")
    for ins in md.disasm(code, 0x114400):
        print(f"  {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")

with open('/mnt/d/vphonewin/fw/vz/AVPBooter.vresearch1.bin', 'rb') as f:
    f.seek(0x14000)
    code = f.read(64)
    print("\nDisassembly of AVPBooter at offset 0x14000 (VBAR?):")
    for ins in md.disasm(code, 0x114000):
        print(f"  {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")
