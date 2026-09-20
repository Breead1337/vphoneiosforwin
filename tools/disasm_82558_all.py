import capstone

md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)

f = open('/mnt/d/vphonewin/fw/cloud/raw/dyld.bin', 'rb')
f.seek(0x82558)
code = f.read(0x180)

print("Disassembly of 0x82558..0x826d8:")
for ins in md.disasm(code, 0x70082558):
    print(f"  {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")
