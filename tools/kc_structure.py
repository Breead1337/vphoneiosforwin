#!/usr/bin/env python3
import struct
KC = "/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin"
d = open(KC, "rb").read()
magic, cput, cpsub, ftype, ncmds, szc, flags, res = struct.unpack_from("<IIIIIIII", d, 0)
print("magic=0x%x filetype=%d (0xc=FILESET,2=EXEC) ncmds=%d flags=0x%x" % (magic, ftype, ncmds, flags))
p = 32; fileset=[]
names={0x2:"SYMTAB",0xb:"DYSYMTAB",0x19:"SEGMENT_64",0x35:"FILESET_ENTRY",0x1e:"LOAD_KEXT?",0x22:"DYLD_INFO",0x80000035:"FILESET_ENTRY"}
for _ in range(ncmds):
    cmd, sz = struct.unpack_from("<II", d, p)
    nm = names.get(cmd, "0x%x"%cmd)
    if cmd == 0x19:
        seg=d[p+8:p+24].split(b"\0")[0].decode(); vm,vs,fo,fs=struct.unpack_from("<QQQQ",d,p+24)
        print("  SEGMENT %-16s vm=0x%-12x foff=0x%-9x size=0x%x" % (seg,vm,fo,fs))
    elif cmd in (0x35,0x80000035):  # LC_FILESET_ENTRY
        vmaddr,fileoff = struct.unpack_from("<QQ", d, p+8)
        entryid_off = struct.unpack_from("<I", d, p+24)[0]
        nm2 = d[p+entryid_off:p+sz].split(b"\0")[0].decode('latin1')
        fileset.append((nm2,vmaddr,fileoff));
    elif cmd == 0x2:
        so,ns,stro,strs=struct.unpack_from("<IIII",d,p+8); print("  SYMTAB nsyms=%d symoff=0x%x"%(ns,so))
    p += sz
print("FILESET entries:", len(fileset))
for nm,vm,fo in fileset[:40]:
    print("  %-40s vm=0x%x foff=0x%x" % (nm,vm,fo))
