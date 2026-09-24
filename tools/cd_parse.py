#!/usr/bin/env python3
# Dump the CodeDirectory of a thin arm64e Mach-O (dyld): fields needed to re-sign a patched page.
import struct, sys, hashlib
path = sys.argv[1]
d = open(path, "rb").read()
ncmds = struct.unpack_from("<I", d, 16)[0]; p = 32
cs_off = cs_size = None
for _ in range(ncmds):
    cmd, csize = struct.unpack_from("<II", d, p)
    if cmd == 0x1d:  # LC_CODE_SIGNATURE
        cs_off, cs_size = struct.unpack_from("<II", d, p+8)
    p += csize
assert cs_off, "no LC_CODE_SIGNATURE"
blob = d[cs_off:cs_off+cs_size]
mg, ln, n = struct.unpack_from(">III", blob, 0)
print("superblob magic=0x%x count=%d off=0x%x size=%d" % (mg, n, cs_off, cs_size))
for i in range(n):
    typ, off = struct.unpack_from(">II", blob, 12 + i*8)
    bmg = struct.unpack_from(">I", blob, off)[0]
    print("  slot type=0x%x off=0x%x magic=0x%x" % (typ, off, bmg))
    if bmg == 0xfade0c02:  # CodeDirectory
        cd = blob[off:]
        (magic, length, version, flags, hashOffset, identOffset, nSpecialSlots,
         nCodeSlots, codeLimit, hashSize, hashType, platform, pageSize, spare2) = struct.unpack_from(">IIIIIIIIIBBBBI", cd, 0)
        print("    CD ver=0x%x flags=0x%x hashOffset=0x%x nSpecial=%d nCode=%d codeLimit=0x%x hashSize=%d hashType=%d pageSize=2^%d len=%d" % (
            version, flags, hashOffset, nSpecialSlots, nCodeSlots, codeLimit, hashSize, hashType, pageSize, length))
        # cdhash = hash of whole CodeDirectory blob
        cdblob = cd[:length]
        cdh = hashlib.sha256(cdblob).digest()[:20]
        print("    cdhash20 =", cdh.hex())
        # verify slot for page containing 0x7e1a8
        pg = 0x7e1a8 >> pageSize
        stored = cd[hashOffset + pg*hashSize: hashOffset + pg*hashSize + hashSize]
        calc = hashlib.sha256(d[pg<<pageSize:(pg+1)<<pageSize]).digest()
        print("    page %d: stored=%s calc=%s match=%s" % (pg, stored.hex()[:16], calc.hex()[:16], stored==calc))
        print("    cs_off=0x%x cd_off_in_file=0x%x hashslot_file_off=0x%x" % (
            cs_off, cs_off+off, cs_off+off+hashOffset+pg*hashSize))
