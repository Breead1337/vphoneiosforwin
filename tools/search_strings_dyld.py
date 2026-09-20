with open("/mnt/d/vphonewin/fw/cloud/raw/dyld.bin", "rb") as f:
    data = f.read()

pos = 0
while True:
    pos = data.find(b"util\x00", pos)
    if pos == -1: break
    print(f"Found 'util\\0' at file offset {pos:#x} (vmaddr {pos:#x} or {0x70000000 + pos:#x})")
    pos += 1

pos = 0
while True:
    pos = data.find(b"root\x00", pos)
    if pos == -1: break
    print(f"Found 'root\\0' at file offset {pos:#x} (vmaddr {pos:#x} or {0x70000000 + pos:#x})")
    pos += 1
