import capstone

md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)

with open('/mnt/d/vphonewin/fw/vz/AVPBooter.vresearch1.bin', 'rb') as f:
    f.seek(0x82400)
    code = f.read(64)
    print("Disassembly of AVPBooter at offset 0x82400 (PC 0x70082400):")
    for ins in md.disasm(code, 0x70082400):
        print(f"  {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")
