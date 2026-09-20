import struct, capstone

with open('/mnt/d/vphonewin/_work/dyld', 'rb') as f:
    code = f.read()

md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)
md.detail = True

targets = [0x105aac, 0x105438, 0x103294, 0x10057c, 0x104310, 0x103230, 0x107ea0]
for target in targets:
    print(f"\n=== Disassembly at dyld + {target:#x} ===")
    start = max(0, target - 20)
    end = min(len(code), target + 8)
    subcode = code[start:end]
    for ins in md.disasm(subcode, start):
        prefix = "-> " if ins.address == target - 4 else "   "
        print(f"{prefix}{ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")
