import struct

with open("/home/ard/vrwork/launchd", "rb") as f:
    data = f.read()

print(f"launchd file size: {len(data)} bytes")
svcs = []
for i in range(0, len(data) - 4, 4):
    w = struct.unpack("<I", data[i:i+4])[0]
    if (w & 0xffe0001f) == 0xd4000001:  # SVC #imm
        imm = (w >> 5) & 0xffff
        svcs.append((i, 0x100000000 + i, imm))

print(f"Total SVC instructions found in launchd binary: {len(svcs)}")
for off, vm, imm in svcs[:30]:
    print(f"  file_off={off:#x} vmaddr={vm:#x} imm={imm:#x} ({imm})")
