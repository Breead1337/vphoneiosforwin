#!/usr/bin/env python3
# Find the cryptex1-sniff failure site in /usr/lib/dyld (thin arm64e Mach-O):
# locate the sniff-related cstrings, find ADRP+ADD xrefs, disassemble around them.
import struct, sys
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_LITTLE_ENDIAN

path = sys.argv[1] if len(sys.argv) > 1 else "/home/ard/vrwork/dyld_hybrid"
d = open(path, "rb").read()
magic = struct.unpack_from("<I", d, 0)[0]
assert magic == 0xfeedfacf, "not thin arm64 macho 0x%x" % magic
ncmds = struct.unpack_from("<I", d, 16)[0]
segs = []            # (name, vmaddr, vmsize, fileoff, filesize)
text_sec = None      # (addr,size,off)
p = 32
for _ in range(ncmds):
    cmd, csize = struct.unpack_from("<II", d, p)
    if cmd == 0x19:  # LC_SEGMENT_64
        segname = d[p+8:p+24].split(b"\0")[0].decode()
        vmaddr, vmsize, fileoff, filesize = struct.unpack_from("<QQQQ", d, p+24)
        segs.append((segname, vmaddr, vmsize, fileoff, filesize))
        nsects = struct.unpack_from("<I", d, p+64)[0]
        sp = p + 72
        for _ in range(nsects):
            sn = d[sp:sp+16].split(b"\0")[0].decode()
            addr, size = struct.unpack_from("<QQ", d, sp+32)
            off = struct.unpack_from("<I", d, sp+48)[0]
            if sn == "__text":
                text_sec = (addr, size, off)
            sp += 80
    p += csize

def foff_to_vm(fo):
    for _, vmaddr, vmsize, fileoff, filesize in segs:
        if fileoff <= fo < fileoff + filesize:
            return vmaddr + (fo - fileoff)
    return None

targets = [b"detecting cryptex1 directory", b"failed to stat cryptex1 canary",
           b"cryptex1 sniff", b"failed to open covered graft point", b"ignition failed"]
str_vms = {}
for t in targets:
    i = d.find(t)
    if i >= 0:
        str_vms[t] = foff_to_vm(i)
        print("str %-40r vm=0x%x" % (t.decode(), str_vms[t]))

taddr, tsize, toff = text_sec
code = d[toff:toff+tsize]
# scan ADRP (+ADD) building targets
xrefs = {}   # str_vm -> list of code vmaddr
for off in range(0, len(code)-8, 4):
    w = struct.unpack_from("<I", code, off)[0]
    if (w & 0x9f000000) == 0x90000000:  # ADRP
        rd = w & 0x1f
        immlo = (w >> 29) & 3
        immhi = (w >> 5) & 0x7ffff
        imm = ((immhi << 2) | immlo)
        if imm & (1 << 20): imm -= (1 << 21)
        pc = taddr + off
        page = (pc & ~0xfff) + (imm << 12)
        w2 = struct.unpack_from("<I", code, off+4)[0]
        if (w2 & 0x7f800000) == 0x11000000 and ((w2 >> 5) & 0x1f) == rd:  # ADD imm, from rd
            add_imm = (w2 >> 10) & 0xfff
            tgt = page + add_imm
            for sv in str_vms.values():
                if sv is not None and tgt == sv:
                    xrefs.setdefault(sv, []).append(pc)

md = Cs(CS_ARCH_ARM64, CS_MODE_LITTLE_ENDIAN)
inv = {v: k for k, v in str_vms.items()}
for sv, pcs in xrefs.items():
    for pc in pcs:
        print("\n==== xref to %r @ 0x%x ====" % (inv.get(sv, b"?").decode(), pc))
        start = pc - taddr - 40
        for ins in md.disasm(code[start:start+140], taddr + start):
            mark = "  <=" if ins.address == pc else ""
            print("  0x%x: %-8s %s%s" % (ins.address, ins.mnemonic, ins.op_str, mark))
