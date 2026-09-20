import capstone

f = open('/mnt/d/vphonewin/fw/cloud/raw/dyld.bin', 'rb')
target = 0x82410
f.seek(target - 32)
code = f.read(96)

md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)
print(f"Disassembly of dyld around {target:#x} (loaded at 0x70082410):")
for ins in md.disasm(code, target - 32):
    prefix = "==> " if ins.address == target or ins.address == target + 8 else "    "
    print(f"{prefix}0x{0x70000000 + ins.address:08x} ({ins.address:#x}): {ins.mnemonic:8s} {ins.op_str}")
