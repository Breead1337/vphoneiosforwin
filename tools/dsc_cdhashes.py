#!/usr/bin/env python3
# Compute cdhash (sha256(CodeDirectory)[:20]) for each dyld shared-cache file and
# report membership in a trust cache. Usage: dsc_cdhashes.py <cache_dir> <tc.bin>
import struct, hashlib, os, sys, glob

cache_dir = sys.argv[1]
tc_path = sys.argv[2] if len(sys.argv) > 2 else "/mnt/d/vphonewin/_work/tc/merged.trst.bin"

# load trust cache cdhash set
td = open(tc_path, "rb").read()
ver, uuid, n = struct.unpack_from("<I16sI", td, 0)
stride = (len(td) - 24) // n
tc_set = {td[24 + i*stride:24 + i*stride + 20] for i in range(n)}
print("TC %s: n=%d stride=%d" % (os.path.basename(tc_path), n, stride))

def cdhash_of(path):
    d = open(path, "rb").read()
    if d[:7] != b"dyld_v1":
        return None, "not-a-dyld-cache (magic %r)" % d[:8]
    cs_off, cs_size = struct.unpack_from("<QQ", d, 40)
    if cs_off == 0 or cs_size == 0 or cs_off + cs_size > len(d):
        return None, "no/invalid code sig (off=%d size=%d flen=%d)" % (cs_off, cs_size, len(d))
    blob = d[cs_off:cs_off + cs_size]
    smg, slen, scount = struct.unpack_from(">III", blob, 0)
    if smg != 0xfade0cc0:
        return None, "not embedded-sig superblob (magic 0x%x)" % smg
    cds = []
    for i in range(scount):
        typ, off = struct.unpack_from(">II", blob, 12 + i*8)
        bmg = struct.unpack_from(">I", blob, off)[0]
        if bmg == 0xfade0c02:
            bl = struct.unpack_from(">I", blob, off + 4)[0]
            cd = blob[off:off + bl]
            cds.append((cd[37], cd))  # cd[37] = hashType
    cd = None
    for ht, c in cds:
        if ht == 2:  # SHA256
            cd = c
    if cd is None and cds:
        cd = cds[0][1]
    if cd is None:
        return None, "no CodeDirectory in superblob"
    return hashlib.sha256(cd).digest()[:20], "ok (%d CDs)" % len(cds)

files = sorted(glob.glob(os.path.join(cache_dir, "dyld_shared_cache_arm64e*")))
missing = []
for f in files:
    b = os.path.basename(f)
    if b.endswith(".symbols"):
        print("  %-45s SKIP (symbols)" % b); continue
    h, note = cdhash_of(f)
    if h is None:
        print("  %-45s -- %s" % (b, note)); continue
    inn = h in tc_set
    if not inn:
        missing.append((b, h))
    print("  %-45s cdhash=%s inTC=%s" % (b, h.hex(), inn))

print("\nMISSING from TC: %d" % len(missing))
for b, h in missing:
    print("  %s %s" % (h.hex(), b))
