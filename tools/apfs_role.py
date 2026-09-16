# set apfs_role (volume superblock +0x3c4) on every APSB block of an APFS container image; fixes the fletcher64 checksum
# usage: python3 apfs_role.py container.img <role hex, 0x10=Preboot> [volname]  (4K blocks)
import struct, sys

ROLE_OFF, NAME_OFF, BS = 0x3C4, 0x2C0, 4096


def fletcher64(b):
    s1 = s2 = 0
    for (w,) in struct.iter_unpack("<I", b):
        s1 = (s1 + w) % 0xFFFFFFFF
        s2 = (s2 + s1) % 0xFFFFFFFF
    c1 = 0xFFFFFFFF - ((s1 + s2) % 0xFFFFFFFF)
    c2 = 0xFFFFFFFF - ((s1 + c1) % 0xFFFFFFFF)
    return struct.pack("<II", c1, c2)


path, role = sys.argv[1], int(sys.argv[2], 0)
name = sys.argv[3].encode() if len(sys.argv) > 3 else None
with open(path, "r+b") as f:
    n = 0
    blk = 0
    while True:
        f.seek(blk * BS)
        b = f.read(BS)
        if len(b) < BS:
            break
        if b[0x20:0x24] == b"APSB" and b[:8] == fletcher64(b[8:]):
            b = bytearray(b)
            b[ROLE_OFF:ROLE_OFF + 2] = struct.pack("<H", role)
            if name:
                b[NAME_OFF:NAME_OFF + 256] = name.ljust(256, b"\0")
            b[:8] = fletcher64(bytes(b[8:]))
            f.seek(blk * BS)
            f.write(b)
            n += 1
            print(f"APSB @ block {blk:#x}: role={role:#x}")
        blk += 1
        if blk > 0x4000 and n:  # mkapfs puts metadata at the start
            break
assert n, "no APSB found"
