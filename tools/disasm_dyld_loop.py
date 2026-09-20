import capstone

f = open('/mnt/d/vphonewin/_work/dyld', 'rb')
md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)

# Disassemble backwards from 0x823f0 to find function entry
target = 0x82300
f.seek(target)
code = f.read(0x150)

print(f"Disassembly of dyld 0x82300..0x82450:")
for ins in md.disasm(code, target):
    print(f"  0x{0x70000000 + ins.address:08x} ({ins.address:#x}): {ins.mnemonic:8s} {ins.op_str}")
