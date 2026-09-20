import capstone

f = open('/mnt/d/vphonewin/_work/dyld', 'rb')
md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)

for target in [0x824fc, 0x82338]:
    f.seek(target)
    code = f.read(64)
    print(f"\nDisassembly of dyld at {target:#x} (0x{0x70000000+target:08x}):")
    for ins in md.disasm(code, target):
        print(f"  0x{0x70000000 + ins.address:08x}: {ins.mnemonic:8s} {ins.op_str}")
