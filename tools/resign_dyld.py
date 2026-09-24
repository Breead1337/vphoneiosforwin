#!/usr/bin/env python3
# Apply one or more code-byte patches to a thin arm64e dyld and RE-SIGN: recompute the
# SHA256 of every affected code page in the CodeDirectory, then the cdhash, so the
# signature matches the patched bytes (interpreter passes exec-time validation).
# Usage: resign_dyld.py <in> <out> <vmaddr>:<hexbytes> [<vmaddr>:<hexbytes> ...]
import struct, sys, hashlib
src, out = sys.argv[1], sys.argv[2]
patches = []
for a in sys.argv[3:]:
    vm, hx = a.split(":")
    patches.append((int(vm, 0), bytes.fromhex(hx)))

d = bytearray(open(src, "rb").read())
# apply patches (print old bytes)
for vm, nb in patches:
    old = bytes(d[vm:vm+len(nb)])
    print("patch 0x%x: %s -> %s" % (vm, old.hex(), nb.hex()))
    d[vm:vm+len(nb)] = nb

# locate CodeDirectory
ncmds = struct.unpack_from("<I", d, 16)[0]; p = 32; cs_off = None
for _ in range(ncmds):
    cmd, csize = struct.unpack_from("<II", d, p)
    if cmd == 0x1d: cs_off, cs_size = struct.unpack_from("<II", d, p+8)
    p += csize
mg, ln, n = struct.unpack_from(">III", d, cs_off); cd_off = None
for i in range(n):
    typ, off = struct.unpack_from(">II", d, cs_off + 12 + i*8)
    if struct.unpack_from(">I", d, cs_off+off)[0] == 0xfade0c02:
        cd_off = cs_off + off
(magic, length, version, flags, hashOffset, identOffset, nSpecialSlots,
 nCodeSlots, codeLimit, hashSize, hashType, platform, pageSize, spare2) = struct.unpack_from(">IIIIIIIIIBBBBI", d, cd_off)
assert hashType == 2 and hashSize == 32
old_cdhash = hashlib.sha256(bytes(d[cd_off:cd_off+length])).digest()[:20]
pages = sorted({vm >> pageSize for vm, _ in patches})
for pg in pages:
    lo = pg << pageSize; hi = min((pg+1) << pageSize, codeLimit)
    h = hashlib.sha256(bytes(d[lo:hi])).digest()
    slot = cd_off + hashOffset + pg*hashSize
    d[slot:slot+hashSize] = h
    print("re-hashed page %d slot@0x%x" % (pg, slot))
new_cdhash = hashlib.sha256(bytes(d[cd_off:cd_off+length])).digest()[:20]
open(out, "wb").write(d)
print("cdhash old =", old_cdhash.hex())
print("cdhash new =", new_cdhash.hex())
open(out + ".cdhash", "w").write(new_cdhash.hex())
