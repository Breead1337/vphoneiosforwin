#!/usr/bin/env python3
# Parse the embedded com.apple.kernel Mach-O (at KC file offset 0x4000) LC_SYMTAB and
# print symbols matching the query words. nlist n_value = absolute vmaddr.
import struct, sys
KC = "/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin"
d = open(KC, "rb").read()
BASEOFF = 0x4000   # com.apple.kernel embedded Mach-O
magic, cput, cpsub, ftype, ncmds, szc, flags, res = struct.unpack_from("<IIIIIIII", d, BASEOFF)
print("kernel Mach-O: magic=0x%x filetype=%d ncmds=%d" % (magic, ftype, ncmds))
p = BASEOFF + 32; symoff=nsyms=stroff=strsize=None
for _ in range(ncmds):
    cmd, sz = struct.unpack_from("<II", d, p)
    if cmd == 0x2:
        symoff, nsyms, stroff, strsize = struct.unpack_from("<IIII", d, p+8)
    p += sz
if symoff is None:
    print("NO LC_SYMTAB in kernel entry"); sys.exit(0)
print("SYMTAB nsyms=%d symoff=0x%x stroff=0x%x" % (nsyms, symoff, stroff))
pats = [w.encode() for w in sys.argv[1:]] or [b"shared_region"]
hits=0
for i in range(nsyms):
    off = symoff + i*16
    n_strx, n_type, n_sect, n_desc, n_value = struct.unpack_from("<IBBHQ", d, off)
    if n_strx == 0: continue
    s = stroff + n_strx; e = d.find(b"\0", s); name = d[s:e]
    if any(pt in name for pt in pats):
        print("0x%016x %s" % (n_value, name.decode('latin1'))); hits+=1
        if hits>150: print("...(truncated)"); break
print("matches:", hits)
