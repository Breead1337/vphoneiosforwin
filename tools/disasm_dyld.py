import struct
import capstone

def main():
    with open("/mnt/d/vphonewin/_work/dyld", "rb") as f:
        data = f.read()

    md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)

    offsets = [0x823c0, 0x91ebc, 0xa8340, 0xc2d20, 0xd12e0, 0xd1370, 0xe06e0, 0xe1470]

    for off in offsets:
        print(f"\n=== OFFSET 0x{off:x} ===")
        chunk = data[off : off + 64]
        for insn in md.disasm(chunk, off):
            print(f"  0x{insn.address:x}: {insn.mnemonic:8s} {insn.op_str}")

if __name__ == '__main__':
    main()
