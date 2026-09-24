#!/usr/bin/env python3
# Parse the research KC's symbol table (LC_SYMTAB) and print symbols relevant to the
# shared region / exec / dyld cache mapping. Flat map: vmaddr already absolute in nlist.
import struct, sys
KC = "/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin"
d = open(KC, "rb").read()
ncmds = struct.unpack_from("<I", d, 16)[0]; p = 32
symoff = nsyms = stroff = strsize = None
for _ in range(ncmds):
    cmd, sz = struct.unpack_from("<II", d, p)
    if cmd == 0x2:  # LC_SYMTAB
        symoff, nsyms, stroff, strsize = struct.unpack_from("<IIII", d, p+8)
    p += sz
if symoff is None:
    print("NO LC_SYMTAB"); sys.exit(0)
print("LC_SYMTAB: nsyms=%d symoff=0x%x stroff=0x%x strsize=0x%x" % (nsyms, symoff, stroff, strsize))
pats = [w.encode() for w in sys.argv[1:]] or [b"shared_region", b"shared_cache", b"commpage",
        b"load_machfile", b"map_shared", b"vm_shared", b"activate_exec", b"shared_file"]
hits = 0
for i in range(nsyms):
    off = symoff + i*16
    if off+16 > len(d): break
    n_strx, n_type, n_sect, n_desc, n_value = struct.unpack_from("<IBBHQ", d, off)
    if n_strx == 0: continue
    s = stroff + n_strx
    e = d.find(b"\0", s)
    name = d[s:e]
    if any(pt in name for pt in pats):
        print("0x%016x %s" % (n_value, name.decode('latin1')))
        hits += 1
        if hits > 120: print("... (truncated)"); break
print("total matches:", hits)
