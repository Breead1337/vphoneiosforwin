import struct, capstone

with open("/mnt/d/vphonewin/fw/cloud/raw/dyld.bin", "rb") as f:
    data = f.read()

print(f"dyld.bin size: {len(data):#x} ({len(data)} bytes)")

md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)

svcs = []
for i in range(0, len(data) - 4, 4):
    w = struct.unpack("<I", data[i:i+4])[0]
    if (w & 0xffe0001f) == 0xd4000001:  # SVC #imm
        imm = (w >> 5) & 0xffff
        svcs.append((i, imm))

print(f"Total SVC instructions in dyld.bin: {len(svcs)}")
for off, imm in svcs[:50]:
    print(f"  offset={off:#x}: imm={imm:#x} ({imm})")
    # disassemble 3 instructions before and 1 instruction after
    start = max(0, off - 12)
    chunk = data[start:off + 8]
    for ins in md.disasm(chunk, start):
        mark = "==> " if ins.address == off else "    "
        print(f"    {mark}{ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")
