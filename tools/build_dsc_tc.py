#!/usr/bin/env python3
# Add every dyld shared-cache file's cdhash to a trust cache and emit both the raw
# merged TC and an IMG4-wrapped StaticTrustCache. Reuses the formats of
# tc_append.py (24B entry: cdhash[20]+<HH>(0xC002,0x3), sorted) and build_static_tc.py.
# usage: build_dsc_tc.py <cache_dir> <merged_in.bin> <merged_out.bin> <static_tc.img4>
import struct, hashlib, os, sys, glob

cache_dir, merged_in, merged_out, img4_out = sys.argv[1:5]

def cdhash_of(path):
    d = open(path, "rb").read()
    if d[:7] != b"dyld_v1":
        return None
    cs_off, cs_size = struct.unpack_from("<QQ", d, 40)
    if not cs_off or cs_off + cs_size > len(d):
        return None
    blob = d[cs_off:cs_off + cs_size]
    smg, slen, scount = struct.unpack_from(">III", blob, 0)
    if smg != 0xfade0cc0:
        return None
    cd = None
    for i in range(scount):
        typ, off = struct.unpack_from(">II", blob, 12 + i*8)
        if struct.unpack_from(">I", blob, off)[0] == 0xfade0c02:
            bl = struct.unpack_from(">I", blob, off + 4)[0]
            c = blob[off:off + bl]
            if c[37] == 2:  # SHA256 CD preferred
                cd = c
            elif cd is None:
                cd = c
    return hashlib.sha256(cd).digest()[:20] if cd else None

# existing entries
d = bytearray(open(merged_in, "rb").read())
ver, uuid, n = struct.unpack_from("<I16sI", d, 0)
assert ver == 2, "unexpected TC version %d" % ver
ents = [bytes(d[24 + i*24:24 + i*24 + 24]) for i in range(n)]
have = {e[:20] for e in ents}

added = 0
for f in sorted(glob.glob(os.path.join(cache_dir, "dyld_shared_cache_arm64e*"))):
    if f.endswith(".symbols"):
        continue
    h = cdhash_of(f)
    if h and h not in have:
        ents.append(h + struct.pack("<HH", 0xC002, 0x3))
        have.add(h); added += 1

ents = sorted(set(ents), key=lambda e: e[:20])
open(merged_out, "wb").write(struct.pack("<I16sI", ver, uuid, len(ents)) + b"".join(ents))
print("merged: %d -> %d entries (+%d), wrote %s" % (n, len(ents), added, merged_out))

# IMG4 wrap (from build_static_tc.py)
def der_len(x):
    if x < 0x80: return bytes([x])
    b = x.to_bytes((x.bit_length()+7)//8, "big"); return bytes([0x80|len(b)]) + b
payload = open(merged_out, "rb").read()
im4p_body = b"\x16\x04IM4P" + b"\x16\x04trst" + b"\x16\x011" + b"\x04"+der_len(len(payload))+payload
im4p = b"\x30"+der_len(len(im4p_body))+im4p_body
img4_body = b"\x16\x04IMG4" + im4p
img4 = b"\x30"+der_len(len(img4_body))+img4_body
open(img4_out, "wb").write(img4)
print("img4: %d bytes (payload %d) -> %s" % (len(img4), len(payload), img4_out))
