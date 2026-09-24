#!/usr/bin/env python3
# Find "out of range bind ordinal" in dyld, locate its code reference, disassemble to see
# what "max" (the count) is derived from (cache image count vs main-exe import count).
import struct, sys
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_LITTLE_ENDIAN
d = open("/home/ard/vrwork/dyld_hybrid", "rb").read()
ncmds = struct.unpack_from("<I", d, 16)[0]; p = 32
segs = []; text = None
for _ in range(ncmds):
    cmd, csize = struct.unpack_from("<II", d, p)
    if cmd == 0x19:
        vm,vs,fo,fs = struct.unpack_from("<QQQQ", d, p+24); segs.append((vm,fo,fs))
        nsects = struct.unpack_from("<I", d, p+64)[0]; sp=p+72
        for _ in range(nsects):
            sn=d[sp:sp+16].split(b"\0")[0].decode(); addr,size=struct.unpack_from("<QQ",d,sp+32); off=struct.unpack_from("<I",d,sp+48)[0]
            if sn=="__text": text=(addr,size,off)
            sp+=80
    p += csize
def fo2vm(fo):
    for vm,foff,fs in segs:
        if foff<=fo<foff+fs: return vm+(fo-foff)
    return None
s = b"out of range bind ordinal"
i = d.find(s); svm = fo2vm(i)
print("string @foff 0x%x vm=0x%x: %r" % (i, svm, d[i:i+45]))
taddr,tsize,toff = text; code = d[toff:toff+tsize]
md = Cs(CS_ARCH_ARM64, CS_MODE_LITTLE_ENDIAN)
regpage={}; hits=[]
for off in range(0,len(code)-4,4):
    w=struct.unpack_from("<I",code,off)[0]; pc=taddr+off
    if (w&0x9f000000)==0x90000000:
        rd=w&0x1f; immlo=(w>>29)&3; immhi=(w>>5)&0x7ffff; imm=(immhi<<2)|immlo
        if imm&(1<<20): imm-=(1<<21)
        regpage[rd]=(pc&~0xfff)+(imm<<12)
    elif (w&0x7f800000)==0x11000000:
        rd=w&0x1f; rn=(w>>5)&0x1f
        if rn in regpage:
            imm=(w>>10)&0xfff
            if w&(1<<22): imm<<=12
            if regpage[rn]+imm==svm: hits.append(pc)
print("xref add sites:", [hex(h) for h in hits])
for h in hits[:2]:
    start=max(0,h-taddr-140)
    print("\n---- around 0x%x ----"%h)
    for ins in md.disasm(code[start:start+240], taddr+start):
        mk = " <=" if ins.address==h else ""
        print("0x%x: %-8s %s%s"%(ins.address,ins.mnemonic,ins.op_str,mk))
