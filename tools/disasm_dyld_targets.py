import capstone

f = open('/mnt/d/vphonewin/_work/dyld', 'rb')
md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)

targets = [0xdc75c, 0xc2d50, 0xc2db4, 0xe0708, 0x9b780, 0x85dc0, 0x89738]
for target in targets:
    f.seek(target - 16)
    code = f.read(64)
    print(f"\n=======================================================")
    print(f"Disassembly around dyld 0x{target:x} (0x{0x70000000+target:08x}):")
    for ins in md.disasm(code, target - 16):
        prefix = "==> " if ins.address == target else "    "
        print(f"{prefix}0x{0x70000000+ins.address:08x} ({ins.address:#x}): {ins.mnemonic:8s} {ins.op_str}")
