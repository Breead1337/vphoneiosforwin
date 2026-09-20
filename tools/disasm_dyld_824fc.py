import capstone

f = open('/mnt/d/vphonewin/_work/dyld', 'rb')
md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)

target = 0x824fc
f.seek(target)
code = f.read(0x120)

print(f"Disassembly of dyld 0x824fc..0x8261c:")
for ins in md.disasm(code, target):
    print(f"  0x{0x70000000 + ins.address:08x} ({ins.address:#x}): {ins.mnemonic:8s} {ins.op_str}")
