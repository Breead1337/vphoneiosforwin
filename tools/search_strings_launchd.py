with open("/home/ard/vrwork/launchd", "rb") as f:
    data = f.read()

pos = 0
while True:
    pos = data.find(b"util\x00", pos)
    if pos == -1: break
    print(f"Found 'util\\0' at file offset {pos:#x} (vmaddr {0x100000000 + pos:#x} or {0x100000 + pos:#x})")
    pos += 1

pos = 0
while True:
    pos = data.find(b"root\x00", pos)
    if pos == -1: break
    print(f"Found 'root\\0' at file offset {pos:#x} (vmaddr {0x100000000 + pos:#x} or {0x100000 + pos:#x})")
    pos += 1
