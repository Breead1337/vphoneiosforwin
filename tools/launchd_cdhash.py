import struct, hashlib, os
d = open("/home/ard/vrwork/launchd_hybrid", "rb").read()
mg = struct.unpack_from("<I", d, 0)[0]
print("macho magic 0x%08x size=%d" % (mg, len(d)))
assert mg == 0xfeedfacf, "not thin arm64 mach-o (maybe fat)"
ncmds = struct.unpack_from("<I", d, 16)[0]; p = 32
cs_off = cs_size = None
for _ in range(ncmds):
    cmd, cs = struct.unpack_from("<II", d, p)
    if cmd == 0x1d:
        cs_off, cs_size = struct.unpack_from("<II", d, p + 8)
    p += cs
if cs_off is None:
    print("NO LC_CODE_SIGNATURE -> unsigned binary!"); raise SystemExit
print("LC_CODE_SIGNATURE off=0x%x size=0x%x" % (cs_off, cs_size))
blob = d[cs_off:cs_off + cs_size]
smg, slen, scount = struct.unpack_from(">III", blob, 0)
print("superblob magic 0x%08x count=%d" % (smg, scount))
cds = []
for i in range(scount):
    typ, off = struct.unpack_from(">II", blob, 12 + i * 8)
    bmg = struct.unpack_from(">I", blob, off)[0]
    if bmg == 0xfade0c02:
        bl = struct.unpack_from(">I", blob, off + 4)[0]
        cd = blob[off:off + bl]
        hashType = cd[37]
        cds.append((hashType, cd))
        print("  CD hashType=%d len=%d" % (hashType, bl))
cd = None
for ht, c in cds:
    if ht == 2:
        cd = c
if cd is None and cds:
    cd = cds[0][1]
cdhash = hashlib.sha256(cd).digest()[:20]
print("launchd cdhash20 =", cdhash.hex())
for f in ["/mnt/d/vphonewin/_work/tc/merged.trst.bin",
          "/mnt/d/vphonewin/_work/tc/os.trst.bin",
          "/home/ard/vrwork/tc_iphone/ios_raw.trst.bin"]:
    td = open(f, "rb").read()
    ver, uuid, n = struct.unpack_from("<I16sI", td, 0)
    stride = (len(td) - 24) // n
    found = any(td[24 + i * stride:24 + i * stride + 20] == cdhash for i in range(n))
    print("  %-24s n=%d stride=%d contains_launchd=%s" % (os.path.basename(f), n, stride, found))
