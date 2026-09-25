import struct, capstone
B="/home/ard/vrwork/init_data_protection"; f=open(B,"rb").read()
ncmds=struct.unpack_from("<I",f,16)[0]; o=32; text=None
for i in range(ncmds):
    cmd,csz=struct.unpack_from("<II",f,o)
    if cmd==0x19:
        nsects=struct.unpack_from("<I",f,o+64)[0]; so=o+72
        for s in range(nsects):
            sname=f[so:so+16].split(b"\0")[0].decode()
            saddr,ssize=struct.unpack_from("<QQ",f,so+32); soff=struct.unpack_from("<I",f,so+48)[0]
            if sname=="__text": text=(saddr,ssize,soff)
            so+=80
    o+=csz
saddr,ssize,soff=text
md=capstone.Cs(capstone.CS_ARCH_ARM64,capstone.CS_MODE_LITTLE_ENDIAN); md.detail=True
insns={ins.address:ins for ins in md.disasm(f[soff:soff+ssize],saddr)}
def dump(a0,a1,tag):
    print("==",tag,"==")
    a=a0
    while a<a1:
        ins=insns.get(a)
        if not ins: a+=4; continue
        # annotate string loads
        note=""
        print("0x%x: %s %s%s"%(ins.address,ins.mnemonic,ins.op_str,note)); a+=4
dump(0x100003650,0x1000036b0,"success target 0x100003650")
print()
dump(0x1000031c4,0x100003210,"fail/log path 0x1000031c4")
