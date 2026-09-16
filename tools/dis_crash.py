import sys, capstone

f = r"D:\vphonewin\fw\cloud\raw\LLB.vresearch101.RELEASE.bin"
base = 0x7006c000
d = open(f, "rb").read()
md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)

addrs = [
    (0x700cd0b0, 0x30, "Frame 6: 0x700cd0dc"),
    (0x700cd830, 0x40, "Frame 5 & 4: 0x700cd84c & 0x700cd8b4"),
    (0x70089ca0, 0x50, "Frame 3 & 2: 0x70089cbc & 0x70089ce0"),
    (0x7008a7a0, 0x30, "Frame 1: 0x7008a7bc (panic callsite)")
]

for start_addr, length, label in addrs:
    off = start_addr - base
    print("=" * 60)
    print(label, f"(file offset {hex(off)})")
    print("=" * 60)
    for i in md.disasm(d[off:off+length], start_addr):
        marker = " <--" if i.address in (0x700cd0dc, 0x700cd84c, 0x700cd8b4, 0x70089cbc, 0x70089ce0, 0x7008a7bc) else ""
        print(f"  {i.address:#x}: {i.bytes.hex()}  {i.mnemonic:<8} {i.op_str}{marker}")
    print()
