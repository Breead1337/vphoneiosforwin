#!/usr/bin/env python3
# Find BL callers of a target address in dyld __text (to trace the cache-setup call graph).
import struct, sys
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_LITTLE_ENDIAN
d = open("/home/ard/vrwork/dyld_hybrid","rb").read()
ncmds=struct.unpack_from("<I",d,16)[0]; p=32; text=None
for _ in range(ncmds):
    cmd,sz=struct.unpack_from("<II",d,p)
    if cmd==0x19:
        vm,vs,fo,fs=struct.unpack_from("<QQQQ",d,p+24); nsects=struct.unpack_from("<I",d,p+64)[0]; sp=p+72
        for _ in range(nsects):
            sn=d[sp:sp+16].split(b"\0")[0].decode(); addr,size=struct.unpack_from("<QQ",d,sp+32); off=struct.unpack_from("<I",d,sp+48)[0]
            if sn=="__text": text=(addr,size,off)
            sp+=80
    p+=sz
taddr,tsize,toff=text; code=d[toff:toff+tsize]
targets=[int(x,0) for x in sys.argv[1:]]
def pro(off):
    for back in range(0,8000,4):
        a=off-back
        if a<0: break
        if struct.unpack_from("<I",code,a)[0]==0xd503237f: return taddr+a
    return None
for tgt in targets:
    callers=[]
    for a in range(0,len(code)-4,4):
        w=struct.unpack_from("<I",code,a)[0]
        if (w&0xfc000000)==0x94000000:  # BL
            imm=w&0x03ffffff
            if imm&(1<<25): imm-=(1<<26)
            if taddr+a+imm*4==tgt: callers.append(taddr+a)
    print("target 0x%x: %d BL callers"%(tgt,len(callers)))
    seen=set()
    for c in callers:
        pr=pro(c-taddr)
        key=pr
        print("   caller@0x%x  in func %s"%(c, hex(pr) if pr else "?"))
