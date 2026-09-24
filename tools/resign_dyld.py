#!/usr/bin/env python3
# Patch dyld byte at 0x7e1a8 (graft-os cbnz -> NOP) AND re-sign: update the page-126
# SHA256 code slot and recompute the cdhash, so the CodeDirectory matches the patched
# bytes (fixes exec-time signature validation). Prints old/new cdhash.
# Usage: resign_dyld.py <in_dyld> <out_dyld>
import struct, sys, hashlib
src, out = sys.argv[1], sys.argv[2]
d = bytearray(open(src, "rb").read())
VM = 0x7e1a8; NOP = b"\x1f\x20\x03\xd5"; EXPECT = bytes.fromhex("97e2ff35")
assert bytes(d[VM:VM+4]) in (EXPECT, NOP), "unexpected bytes at 0x%x: %s" % (VM, d[VM:VM+4].hex())
d[VM:VM+4] = NOP
# locate CodeDirectory
ncmds = struct.unpack_from("<I", d, 16)[0]; p = 32; cs_off = None
for _ in range(ncmds):
    cmd, csize = struct.unpack_from("<II", d, p)
    if cmd == 0x1d: cs_off, cs_size = struct.unpack_from("<II", d, p+8)
    p += csize
blob_off = cs_off
mg, ln, n = struct.unpack_from(">III", d, blob_off)
cd_off = None
for i in range(n):
    typ, off = struct.unpack_from(">II", d, blob_off + 12 + i*8)
    if struct.unpack_from(">I", d, blob_off+off)[0] == 0xfade0c02:
        cd_off = blob_off + off
assert cd_off
(magic, length, version, flags, hashOffset, identOffset, nSpecialSlots,
 nCodeSlots, codeLimit, hashSize, hashType, platform, pageSize, spare2) = struct.unpack_from(">IIIIIIIIIBBBBI", d, cd_off)
assert hashType == 2 and hashSize == 32
pg = VM >> pageSize
# recompute page hash over the patched bytes (respect codeLimit for the last page)
lo = pg << pageSize; hi = min((pg+1) << pageSize, codeLimit)
newhash = hashlib.sha256(bytes(d[lo:hi])).digest()
slot = cd_off + hashOffset + pg*hashSize
old_cdhash = hashlib.sha256(bytes(d[cd_off:cd_off+length])).digest()[:20]
d[slot:slot+hashSize] = newhash
new_cdhash = hashlib.sha256(bytes(d[cd_off:cd_off+length])).digest()[:20]
open(out, "wb").write(d)
print("patched 0x%x -> NOP; page %d slot@0x%x updated" % (VM, pg, slot))
print("cdhash old =", old_cdhash.hex())
print("cdhash new =", new_cdhash.hex())
open(out + ".cdhash", "w").write(new_cdhash.hex())
