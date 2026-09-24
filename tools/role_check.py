#!/usr/bin/env python3
# Verify apfs_role of each volume in a test container by locating volname fields.
# In apfs_superblock_t, apfs_volname[256] is followed by apfs_next_doc_id(4) then apfs_role(u16).
import struct, sys
d = open(sys.argv[1] if len(sys.argv) > 1 else "/tmp/t6.apfs", "rb").read()
want = {b"Preboot": 0x10, b"System": 0x1, b"Data": 0x40, b"Update": 0xc0, b"xART": 0x100, b"Hardware": 0x140}
for name, exp in want.items():
    off = d.find(name + b"\x00")
    if off < 0:
        print(f"{name.decode():9} volname NOT FOUND"); continue
    role = struct.unpack_from("<H", d, off + 256 + 4)[0]
    ok = "OK" if role == exp else f"MISMATCH exp=0x{exp:x}"
    print(f"{name.decode():9} @0x{off:x} role=0x{role:x} {ok}")
