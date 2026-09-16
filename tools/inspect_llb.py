import struct

with open("/mnt/d/vphonewin/fw/cloud/raw/LLB.vresearch101.RELEASE.bin", "rb") as f:
    rel_data = f.read()

# Read 64-bit values at 0x2f8, 0x300, 0x308, 0x310, etc.
for off in range(0x2e0, 0x340, 8):
    v = struct.unpack("<Q", rel_data[off:off+8])[0]
    print(f"literal at {hex(off)}: {hex(v)}")

# Also let's disassemble the first 16 instructions using capstone if available
try:
    from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM
    md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
    for i in md.disasm(rel_data[:64], 0):
        print(f"0x{i.address:x}:\t{i.mnemonic}\t{i.op_str}")
except Exception as e:
    print("capstone error:", e)
