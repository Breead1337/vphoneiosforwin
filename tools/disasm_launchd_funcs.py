import capstone

f = open('/home/ard/vrwork/launchd', 'rb')
md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)

targets = [0x1485ac, 0x146f48, 0x15a270, 0x10ed28, 0x114d8c, 0x147bc8, 0x15a330]

for target in targets:
    file_offset = target - 0x100000
    f.seek(file_offset)
    code = f.read(48)
    print(f"\n=======================================================")
    print(f"Disassembly of function at {target:#x} (file offset {file_offset:#x}):")
    for ins in md.disasm(code, target):
        print(f"  {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")
