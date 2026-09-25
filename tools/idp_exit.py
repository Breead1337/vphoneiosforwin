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
def dump(a0,n,tag):
    print("==",tag,"=="); a=a0
    for _ in range(n):
        ins=insns.get(a)
        if ins: print("0x%x: %s %s"%(a,ins.mnemonic,ins.op_str))
        a+=4
dump(0x100003b00,20,"common sink 0x100003b00 (w28=exit code?)")
print(); dump(0x100003214,14,"0x100003214")
# also find where main's gigalocker function is entered: scan back from 0x1000035e8 for prologue (stp x29 / pacibsp)
print("\n== prologue search back from 0x1000035e8 ==")
a=0x1000035e8
while a>0x100000948:
    ins=insns.get(a)
    if ins and ins.mnemonic in ("pacibsp","paciasp"):
        print("func entry ~0x%x: %s"%(a,ins.mnemonic)); break
    a-=4
