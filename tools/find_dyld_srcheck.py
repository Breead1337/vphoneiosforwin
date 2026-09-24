#!/usr/bin/env python3
# Find where dyld issues shared_region_check_np (syscall 294=0x126) and disassemble the
# caller's decision (the branch that launchd takes but the child skips). Also find the
# read of sharedCacheBaseAddress / the "cache already present" check.
import struct, sys
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_LITTLE_ENDIAN
d = open("/home/ard/vrwork/dyld_hybrid","rb").read()
ncmds=struct.unpack_from("<I",d,16)[0]; p=32; text=None
for _ in range(ncmds):
    cmd,sz=struct.unpack_from("<II",d,p)
    if cmd==0x19:
        vm,vs,fo,fs=struct.unpack_from("<QQQQ",d,p+24)
        nsects=struct.unpack_from("<I",d,p+64)[0]; sp=p+72
        for _ in range(nsects):
            sn=d[sp:sp+16].split(b"\0")[0].decode(); addr,size=struct.unpack_from("<QQ",d,sp+32); off=struct.unpack_from("<I",d,sp+48)[0]
            if sn=="__text": text=(addr,size,off)
            sp+=80
    p+=sz
taddr,tsize,toff=text; code=d[toff:toff+tsize]
# find 'svc #0x80' (0xd4001001) preceded by mov x16,#0x126
md=Cs(CS_ARCH_ARM64,CS_MODE_LITTLE_ENDIAN)
sites=[]
for a in range(0,len(code)-4,4):
    w=struct.unpack_from("<I",code,a)[0]
    # movz w16,#0x126 : 0x52800000|(imm<<5)|16 ; imm=0x126 -> 0x52800000|(0x126<<5)|16
    if w==(0x52800000|(0x126<<5)|16) or w==(0xd2800000|(0x126<<5)|16):
        sites.append(taddr+a)
print("shared_region_check_np (x16=0x126) load sites:", [hex(s) for s in sites])
for s in sites:
    st=max(0,s-taddr-80)
    print("\n---- caller around 0x%x ----"%s)
    for ins in md.disasm(code[st:st+160], taddr+st):
        mk=" <=" if ins.address==s else ""
        print("0x%x: %-8s %s%s"%(ins.address,ins.mnemonic,ins.op_str,mk))
