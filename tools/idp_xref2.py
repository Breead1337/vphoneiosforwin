import struct, capstone
B="/home/ard/vrwork/init_data_protection"
f=open(B,"rb").read()
ncmds=struct.unpack_from("<I",f,16)[0]
o=32; text=None
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
insns=list(md.disasm(f[soff:soff+ssize],saddr))
idx={ins.address:i for i,ins in enumerate(insns)}
TARGS={0x10001a68b:"failed_init",0x10001a9dc:"doesnt_exist",0x10001a9b0:"gl_exists?",0x10001a63f:"?"}
adrp={}
hits=[]
for i,ins in enumerate(insns):
    if ins.mnemonic=="adrp":
        adrp[ins.reg_name(ins.operands[0].reg)]=ins.operands[1].imm
    elif ins.mnemonic in ("add","adr") and len(ins.operands)>=2:
        try:
            if ins.mnemonic=="add" and len(ins.operands)==3 and ins.operands[2].type==capstone.CS_OP_IMM:
                bn=ins.reg_name(ins.operands[1].reg)
                if bn in adrp:
                    va=adrp[bn]+ins.operands[2].imm
                    # match any string in the cstring page range with known offsets
                    if 0x10001a000<=va<=0x10001b000:
                        hits.append((i,va))
        except: pass
print("cstring-page refs:",len(hits))
for i,va in hits:
    # print the string bytes
    fo=va-0x100000000
    sb=f[fo:fo+48].split(b"\0")[0]
    print("\n0x%x -> 0x%x %r"%(insns[i].address,va,sb[:46]))
    if b"gigalock" in sb.lower() or b"doesn" in sb.lower() or b"nitiali" in sb or b"artition" in sb:
        lo=max(0,i-10); hi=min(len(insns),i+12)
        for j in range(lo,hi):
            m="  >>" if j==i else "    "
            print("%s0x%x: %s %s"%(m,insns[j].address,insns[j].mnemonic,insns[j].op_str))
