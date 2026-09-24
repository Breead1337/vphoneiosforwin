#!/usr/bin/env python3
# Find ADRP+ADD sites in dyld __text that compute given code addresses (function-pointer
# setup for the private/shared cache-map strategy dispatch).
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
targets=[int(x,0) for x in sys.argv[1:]] or [0x62c10,0x63c94]
md=Cs(CS_ARCH_ARM64,CS_MODE_LITTLE_ENDIAN)
regpage=[None]*32
def pro(off):
    for back in range(0,9000,4):
        a=off-back
        if a<0: break
        if struct.unpack_from("<I",code,a)[0]==0xd503237f: return taddr+a
    return None
found={t:[] for t in targets}
for a in range(0,len(code)-4,4):
    w=struct.unpack_from("<I",code,a)[0]
    if (w&0x9f000000)==0x90000000:
        rd=w&0x1f; immlo=(w>>29)&3; immhi=(w>>5)&0x7ffff; imm=(immhi<<2)|immlo
        if imm&(1<<20): imm-=(1<<21)
        regpage[rd]=((taddr+a)&~0xfff)+(imm<<12)
    elif (w&0xff800000)==0x91000000:
        rn=(w>>5)&0x1f; rd=w&0x1f
        if regpage[rn] is not None:
            sh=(w>>22)&3; imm12=(w>>10)&0xfff; val=regpage[rn]+(imm12<<(12 if sh==1 else 0))
            if val in found: found[val].append(taddr+a)
        if rd!=rn: regpage[rd]=None
for t in targets:
    print("func 0x%x referenced (ADRP+ADD) at: %s"%(t,[hex(x) for x in found[t]]))
    for r in found[t]:
        print("   ref@0x%x in func %s"%(r,hex(pro(r-taddr)) if pro(r-taddr) else "?"))
