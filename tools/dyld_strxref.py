#!/usr/bin/env python3
# Robust ADRP+ADD xref finder for an arbitrary string in dyld, with disassembly around each.
import struct, sys
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_LITTLE_ENDIAN
d = open("/home/ard/vrwork/dyld_hybrid","rb").read()
ncmds=struct.unpack_from("<I",d,16)[0]; p=32; segs=[]; text=None
for _ in range(ncmds):
    cmd,sz=struct.unpack_from("<II",d,p)
    if cmd==0x19:
        vm,vs,fo,fs=struct.unpack_from("<QQQQ",d,p+24); segs.append((vm,fo,fs)); nsects=struct.unpack_from("<I",d,p+64)[0]; sp=p+72
        for _ in range(nsects):
            sn=d[sp:sp+16].split(b"\0")[0].decode(); addr,size=struct.unpack_from("<QQ",d,sp+32); off=struct.unpack_from("<I",d,sp+48)[0]
            if sn=="__text": text=(addr,size,off)
            sp+=80
    p+=sz
def fo2vm(fo):
    for vm,foff,fs in segs:
        if foff<=fo<foff+fs: return vm+(fo-foff)
    return None
S=sys.argv[1].encode()
i=d.find(S); svm=fo2vm(i)
print("string %r @foff 0x%x vm=0x%x"%(S,i,svm))
taddr,tsize,toff=text; code=d[toff:toff+tsize]
md=Cs(CS_ARCH_ARM64,CS_MODE_LITTLE_ENDIAN); regpage=[None]*32; hits=[]
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
            if val==svm: hits.append(taddr+a)
        if rd!=rn: regpage[rd]=None
print("xref sites:",[hex(h) for h in hits])
W=int(sys.argv[2]) if len(sys.argv)>2 else 120
for h in hits[:3]:
    st=max(0,h-taddr-40)
    print("\n---- around 0x%x ----"%h)
    for ins in md.disasm(code[st:st+W*4], taddr+st):
        print("0x%x: %-8s %s%s"%(ins.address,ins.mnemonic,ins.op_str," <=" if ins.address==h else ""))
