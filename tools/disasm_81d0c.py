import capstone

md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)

f = open('/mnt/d/vphonewin/fw/cloud/raw/dyld.bin', 'rb')
f.seek(0x81d0c)
code = f.read(64)
print("Disassembly of dyld 0x70081d0c:")
for ins in md.disasm(code, 0x70081d0c):
    print(f"  {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")
