import struct, capstone
B="/home/ard/vrwork/init_data_protection"
f=open(B,"rb").read()
ncmds=struct.unpack_from("<I",f,16)[0]
o=32; text=None; segs=[]
for i in range(ncmds):
    cmd,csz=struct.unpack_from("<II",f,o)
    if cmd==0x19:
        segname=f[o+8:o+24].split(b"\0")[0].decode()
        vmaddr,vmsize,foff,fsize=struct.unpack_from("<QQQQ",f,o+24)
        nsects=struct.unpack_from("<I",f,o+64)[0]
        segs.append((segname,vmaddr,foff,fsize))
        so=o+72
        for s in range(nsects):
            sname=f[so:so+16].split(b"\0")[0].decode()
            saddr,ssize=struct.unpack_from("<QQ",f,so+32); soff=struct.unpack_from("<I",f,so+48)[0]
            if sname=="__text": text=(saddr,ssize,soff)
            so+=80
    o+=csz
print("segments:",[(n,hex(a)) for n,a,_,_ in segs])
print("text:",[hex(x) for x in text])
saddr,ssize,soff=text
md=capstone.Cs(capstone.CS_ARCH_ARM64,capstone.CS_MODE_LITTLE_ENDIAN); md.detail=True
STRPAGE=0x10001a000
insns=list(md.disasm(f[soff:soff+ssize],saddr))
print("n insns:",len(insns))
# count adrp targeting the string page(s) 0x100019000-0x10001b000
cnt=0
for i,ins in enumerate(insns):
    if ins.mnemonic=="adrp":
        try:
            tgt=ins.operands[1].imm
            if 0x100018000<=tgt<=0x10001c000:
                cnt+=1
                if cnt<=12:
                    nxt=insns[i+1] if i+1<len(insns) else None
                    print("adrp 0x%x -> page 0x%x ; next: %s %s"%(ins.address,tgt, nxt.mnemonic if nxt else "?", nxt.op_str if nxt else ""))
        except Exception as e: pass
print("adrp-to-string-page count:",cnt)
