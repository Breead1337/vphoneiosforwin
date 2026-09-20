import capstone

md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)

f = open('/mnt/d/vphonewin/fw/cloud/raw/dyld.bin', 'rb')
f.seek(0x823b0)
code = f.read(0x90)
print("Disassembly of dyld 0x700823b0 - 0x70082440:")
for ins in md.disasm(code, 0x700823b0):
    print(f"  {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")
