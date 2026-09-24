#!/usr/bin/env python3
# NOP the graft-os fatal branch in /usr/lib/dyld (libignition): at vmaddr 0x7e1a8
# `cbnz w23, ...` -> NOP, so the OS-cryptex graft failure becomes non-fatal and
# ignition continues (our dyld cache is on the classic path; real graft not needed).
# Only __TEXT code is changed, NOT the CodeDirectory, so dyld's cdhash is unchanged
# (trust cache stays valid); the patched page's hash mismatch is covered by the
# kernel's cs_invalid_page bypass. Usage: patch_dyld_cryptex.py <dyld> [--apply]
import struct, sys

path = sys.argv[1]
apply = "--apply" in sys.argv
VM = 0x7e1a8
NOP = b"\x1f\x20\x03\xd5"
EXPECT = bytes.fromhex("97e2ff35")   # cbnz w23, #0x7ddf8 (verified via capstone)

d = bytearray(open(path, "rb").read())
assert struct.unpack_from("<I", d, 0)[0] == 0xfeedfacf, "not thin arm64 macho"
ncmds = struct.unpack_from("<I", d, 16)[0]
segs = []; p = 32
for _ in range(ncmds):
    cmd, csize = struct.unpack_from("<II", d, p)
    if cmd == 0x19:
        name = d[p+8:p+24].split(b"\0")[0].decode()
        vmaddr, vmsize, fileoff, filesize = struct.unpack_from("<QQQQ", d, p+24)
        segs.append((name, vmaddr, fileoff, filesize))
    p += csize
foff = None
for name, vmaddr, fileoff, filesize in segs:
    if vmaddr <= VM < vmaddr + filesize:
        foff = fileoff + (VM - vmaddr); seg = name; break
assert foff is not None, "vmaddr not mapped"
cur = bytes(d[foff:foff+4])
print("seg=%s vm=0x%x foff=0x%x bytes=%s (expect %s = cbnz w23)" % (seg, VM, foff, cur.hex(), EXPECT.hex()))
if cur == NOP:
    print("already patched (NOP)"); sys.exit(0)
if cur != EXPECT:
    print("!! unexpected bytes, aborting"); sys.exit(1)
if apply:
    d[foff:foff+4] = NOP
    open(path, "wb").write(d)
    print("PATCHED -> NOP at foff 0x%x" % foff)
else:
    print("(dry run; pass --apply to write)")
