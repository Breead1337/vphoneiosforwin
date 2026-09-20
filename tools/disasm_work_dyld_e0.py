import capstone

with open('/mnt/d/vphonewin/_work/dyld', 'rb') as f:
    f.seek(0xe0bd0 - 32)
    code = f.read(128)

md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)
print("Disassembly of _work/dyld at 0xe0bd0:")
for ins in md.disasm(code, 0xe0bd0 - 32):
    prefix = "==> " if ins.address == 0xe0bd0 else "    "
    print(f"{prefix}{ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")
