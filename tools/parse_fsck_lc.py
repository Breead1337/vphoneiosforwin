#!/usr/bin/env python3
import struct, sys
d = open(sys.argv[1] if len(sys.argv)>1 else "/home/ard/vrwork/fsck.bin","rb").read()
magic, cputype, cpusub, ftype, ncmds, szcmds, flags, res = struct.unpack_from("<IIIIIIII", d, 0)
print("magic=0x%x ncmds=%d filetype=%d flags=0x%x" % (magic, ncmds, ftype, flags))
p = 32; ndylib=0; linkedit=None; text=None
names = {0x19:"SEGMENT_64",0xc:"LOAD_DYLIB",0x1d:"CODE_SIGNATURE",0x22:"DYLD_INFO_ONLY",
         0x80000022:"DYLD_INFO_ONLY",0x1f:"MAIN",0x34:"DYLD_CHAINED_FIXUPS",0x33:"DYLD_EXPORTS_TRIE",
         0xd:"ID_DYLIB",0x26:"FUNCTION_STARTS",0x29:"DATA_IN_CODE",0x2:"SYMTAB",0xb:"DYSYMTAB",0x1b:"UUID"}
for _ in range(ncmds):
    cmd, sz = struct.unpack_from("<II", d, p)
    nm = names.get(cmd, "0x%x"%cmd)
    if cmd == 0x19:
        seg = d[p+8:p+24].split(b"\0")[0].decode(); vm,vs,fo,fs = struct.unpack_from("<QQQQ",d,p+24)
        print("  SEGMENT %-12s vm=0x%-9x fileoff=0x%-8x filesize=0x%x" % (seg, vm, fo, fs))
        if seg=="__LINKEDIT": linkedit=(vm,fo,fs)
        if seg=="__TEXT": text=(vm,fo,fs)
    elif cmd == 0xc: ndylib+=1; print("  LOAD_DYLIB:", d[p+struct.unpack_from('<I',d,p+8)[0]:p+sz].split(b'\0')[0].decode('latin1'))
    elif cmd in (0x34,):
        off,size=struct.unpack_from("<II",d,p+8); print("  CHAINED_FIXUPS off=0x%x size=0x%x"%(off,size))
    elif cmd in (0x22,0x80000022):
        print("  DYLD_INFO bind/lazy present")
    elif cmd == 0x1d:
        off,size=struct.unpack_from("<II",d,p+8); print("  CODE_SIGNATURE off=0x%x size=0x%x (codeLimit)"%(off,size))
    else:
        print("  ", nm)
    p += sz
print("total LC_LOAD_DYLIB =", ndylib, "| __LINKEDIT:", linkedit, "| filesize=", len(d))
