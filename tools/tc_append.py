#!/usr/bin/env python3
# tc_append.py TC_PATH CDHASH_HEX [CDHASH_HEX ...] — insert one or more 24-byte
# entries into the TrustCache v2 payload (see _work/tc/os.trst.bin), bumps
# nentries in the header, keeps existing entries sorted (XNU expects binary
# search — insertion into ordered set required).
# hashtype = 0xC002 (same as observed on existing entries, session 46b),
# flags = 0x0 (no special caps).
import struct, sys

def load(path):
    d = bytearray(open(path, 'rb').read())
    ver, uuid, n = struct.unpack_from('<I16sI', d, 0)
    assert ver == 2
    return d, ver, uuid, n

def dump(path, ver, uuid, entries):
    entries = sorted(set(entries), key=lambda e: e[:20])
    hdr = struct.pack('<I16sI', ver, uuid, len(entries))
    open(path, 'wb').write(hdr + b''.join(entries))

def entries(d, n):
    out = []
    o = 24
    for _ in range(n):
        out.append(bytes(d[o:o+24]))
        o += 24
    return out

if __name__ == '__main__':
    tc_path = sys.argv[1]
    d, ver, uuid, n = load(tc_path)
    ents = entries(d, n)
    added = 0
    for hex_hash in sys.argv[2:]:
        cdh = bytes.fromhex(hex_hash)
        assert len(cdh) == 20
        new = cdh + struct.pack('<HH', 0xC002, 0x3)  # hashtype=0xC002, flags=0x3 (same как оригинал fsck slot #5)
        if new not in ents:
            ents.append(new)
            added += 1
    dump(tc_path, ver, uuid, ents)
    print(f'{tc_path}: was {n} entries, added {added}, now {len(ents)}')
