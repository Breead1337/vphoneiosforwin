import struct, sys
try:
    import capstone
except Exception as e:
    print("no capstone", e); sys.exit(1)
B="/home/ard/vrwork/init_data_protection"
f=open(B,"rb").read()
magic,cput,cpus,ftype,ncmds,szcmds,flags,res=struct.unpack_from("<IiiIIIII",f,0)
segs=[]; text=None; cstr=[]
off=32
for i in range(ncmds):
    cmd,csz=struct.unpack_from("<II",f,off)
    if cmd==0x19:
        name=f[off+8:off+24].split(b"\0")[0].decode()
        vmaddr,vmsize,foff,fsize=struct.unpack_from("<QQQQ",f,off+24)
        nsects=struct.unpack_from("<I",f,off+64)[0]
        so=off+72
        for s in range(nsects):
            sname=f[so:so+16].split(b"\0")[0].decode()
            saddr,ssize=struct.unpack_from("<QQ",f,so+32)
            soff=struct.unpack_from("<I",f,so+48)[0]
            segs.append((name,sname,saddr,ssize,soff))
            if sname=="__text": text=(saddr,ssize,soff)
            if sname in ("__cstring","__const","__oslogstring"): cstr.append((saddr,ssize,soff))
            so+=80
    off+=csz
def foff_to_va(fo):
    for name,sname,saddr,ssize,soff in segs:
        if soff<=fo<soff+ssize: return saddr+(fo-soff)
    return None
# target strings (file offsets from grep)
targets={109020:"doesnt_exist",108171:"failed_init"}
tva={foff_to_va(o):n for o,n in targets.items()}
print("string VAs:",{hex(k):v for k,v in tva.items() if k})
# scan __text for ADRP+ADD/LDR producing these VAs
saddr,ssize,soff=text
code=f[soff:soff+ssize]
md=capstone.Cs(capstone.CS_ARCH_ARM64,capstone.CS_MODE_LITTLE_ENDIAN)
md.detail=True
# simple: track adrp results per reg then add
insns=list(md.disasm(code,saddr))
adrp={}
hits=[]
for idx,ins in enumerate(insns):
    if ins.mnemonic=="adrp":
        try:
            rd=ins.operands[0].reg; imm=ins.operands[1].imm
            adrp[ins.reg_name(rd)]=imm
        except: pass
    elif ins.mnemonic in ("add","ldr") and len(ins.operands)>=2:
        try:
            if ins.mnemonic=="add" and ins.operands[2].type==capstone.arm64.ARM64_OP_IMM:
                base=ins.operands[1].reg; imm=ins.operands[2].imm
                bn=ins.reg_name(base)
                if bn in adrp:
                    va=adrp[bn]+imm
                    if va in tva:
                        hits.append((ins.address,tva[va],idx))
        except: pass
print("xref hits:",[(hex(a),n) for a,n,_ in hits])
# disassemble around each hit
for addr,n,idx in hits:
    print("\n==== around %s (%s) ===="%(hex(addr),n))
    for j in range(max(0,idx-18),min(len(insns),idx+8)):
        ins=insns[j]
        print("0x%x: %s %s"%(ins.address,ins.mnemonic,ins.op_str))
