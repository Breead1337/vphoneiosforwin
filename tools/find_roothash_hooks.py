#!/usr/bin/env python3
# Find prologue VAs of APFS root-hash / seal / snapshot funcs in the release KC.
# Flat map for this KC: vmaddr = 0xfffffe0007004000 + fileoff (verified via LC_SEGMENT_64).
# Disassemble __TEXT_EXEC, find ADRP+ADD -> each func's __func__ cstring, scan back to pacibsp.
import struct, capstone, sys
KC = sys.argv[1] if len(sys.argv) > 1 else "/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin"
BASE = 0xfffffe0007004000
data = open(KC, "rb").read()
# auto-locate __TEXT_EXEC from LC_SEGMENT_64
TEXT_EXEC_FOFF = TEXT_EXEC_SIZE = None
ncmds = struct.unpack_from("<I", data, 16)[0]; p = 32
for _ in range(ncmds):
    cmd, cmdsize = struct.unpack_from("<II", data, p)
    if cmd == 0x19 and data[p+8:p+24].split(b"\0")[0] == b"__TEXT_EXEC":
        vmaddr, vmsize, fileoff, filesize = struct.unpack_from("<QQQQ", data, p+24)
        TEXT_EXEC_FOFF, TEXT_EXEC_SIZE = fileoff, filesize
    p += cmdsize
TEXT_EXEC_VA = BASE + TEXT_EXEC_FOFF
print(f"KC={KC} __TEXT_EXEC foff=0x{TEXT_EXEC_FOFF:x} size=0x{TEXT_EXEC_SIZE:x} va=0x{TEXT_EXEC_VA:x}")

# resolve string file offsets by literal search (exact anchors)
NAMES = [
    b"is_root_hash_authentication_required_ios",  # search longer first
    b"is_root_hash_authentication_required",
    b"authapfs_seal_is_broken_full",
    b"authapfs_seal_is_broken",
    b"apfs_find_named_root_snapshot_xid",
]
str_va = {}
for nm in NAMES:
    o = data.find(nm + b"\x00")
    if o < 0: o = data.find(nm)
    if o >= 0:
        str_va[nm.decode()] = BASE + o
        print(f"str {nm.decode():45s} foff=0x{o:x} va=0x{BASE+o:x}")
    else:
        print(f"str {nm.decode()} NOT FOUND")

targets = set(str_va.values())
code = data[TEXT_EXEC_FOFF:TEXT_EXEC_FOFF+TEXT_EXEC_SIZE]

# Manual ADRP+ADD decode (capstone stops on PAC insns). Also ADRP+LDR(imm) for pointer loads.
refs = {va: [] for va in targets}
adrp_page = [None]*32  # per-reg last adrp page VA
n = len(code)
for a in range(0, n-3, 4):
    w = struct.unpack_from("<I", code, a)[0]
    if (w & 0x9f000000) == 0x90000000:      # ADRP
        rd = w & 0x1f
        immlo = (w >> 29) & 3
        immhi = (w >> 5) & 0x7ffff
        imm = (immhi << 2) | immlo
        if imm & (1 << 20): imm -= (1 << 21)  # sign-extend 21-bit
        pc = TEXT_EXEC_VA + a
        adrp_page[rd] = (pc & ~0xfff) + (imm << 12)
    elif (w & 0xff800000) == 0x91000000:     # ADD (imm, 64-bit)
        rn = (w >> 5) & 0x1f
        rd = w & 0x1f
        if adrp_page[rn] is not None:
            sh = (w >> 22) & 3
            imm12 = (w >> 10) & 0xfff
            val = adrp_page[rn] + (imm12 << (12 if sh == 1 else 0))
            if val in refs:
                refs[val].append(TEXT_EXEC_VA + a)
        if rd != rn:
            adrp_page[rd] = None
print("scanned __TEXT_EXEC words:", n//4)

def find_prologue(ref_pc):
    off = ref_pc - TEXT_EXEC_VA
    for back in range(0, 4000, 4):
        a = off - back
        if a < 0: break
        w = struct.unpack_from("<I", code, a)[0]
        if w == 0xd503237f:  # pacibsp
            return TEXT_EXEC_VA + a
    return None

for lbl, va in str_va.items():
    rs = refs.get(va, [])
    pros = []
    for r in rs:
        p = find_prologue(r)
        if p and p not in pros: pros.append(p)
    print(f"\n### {lbl}  refs={len(rs)}  prologues={[hex(p) for p in pros]}")
    for r in rs[:8]:
        p = find_prologue(r)
        print(f"    ref@0x{r:x} -> pro {hex(p) if p else 'NONE'}")
