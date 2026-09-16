import sys, struct

with open(r"D:\vphonewin\fw\vz\VirtualMachine.arm64e", "rb") as f:
    data = f.read()

for target in [0x400000, 0x500000, 0x600000]:
    t_bytes = struct.pack("<Q", target)
    idx = 0
    while True:
        pos = data.find(t_bytes, idx)
        if pos == -1:
            break
        print(f"=== Found {hex(target)} at offset {hex(pos)} ===")
        start = max(0, pos - 32)
        for i in range(start, min(len(data), pos + 48), 8):
            v = struct.unpack("<Q", data[i:i+8])[0]
            marker = " <--" if i == pos else ""
            print(f"  +{hex(i)}: {hex(v)}{marker}")
        idx = pos + 8
