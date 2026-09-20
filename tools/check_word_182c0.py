import struct

with open('/home/ard/vrwork/launchd', 'rb') as f:
    f.seek(0x182c0)
    w = struct.unpack('<I', f.read(4))[0]
    print(f"Word at 0x182c0: {hex(w)}")
    print(f"Is SVC? {(w & 0xffe0001f) == 0xd4000001}")
