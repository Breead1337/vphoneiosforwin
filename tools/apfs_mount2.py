import struct, capstone
KC="/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin"
f=open(KC,"rb").read(); BASE=0xfffffe0007004000
def find_str(s):
    o=f.find(s.encode()); return (BASE+o) if o>=0 else None
s1=find_str("setting dev block size")
print("str:",hex(s1))
TXT_VA=0xfffffe000887aa00; TXT_FOFF=0x1876a00; TXT_SZ=0x147b50
md=capstone.Cs(capstone.CS_ARCH_ARM64,capstone.CS_MODE_LITTLE_ENDIAN); md.detail=True; md.skipdata=True
code=f[TXT_FOFF:TXT_FOFF+TXT_SZ]
insns=list(md.disasm(code,TXT_VA))
print("insns:",len(insns))
adrp={}; xref=[]
for i,ins in enumerate(insns):
    if ins.mnemonic=="adrp":
        try: adrp[ins.reg_name(ins.operands[0].reg)]=ins.operands[1].imm
        except: pass
    elif ins.mnemonic in ("add",) and len(ins.operands)==3 and ins.operands[2].type==capstone.CS_OP_IMM:
        try:
            bn=ins.reg_name(ins.operands[1].reg)
            if bn in adrp:
                va=adrp[bn]+ins.operands[2].imm
                if s1 and abs(va-s1)<0x30: xref.append(i)
        except: pass
print("xrefs:",[hex(insns[i].address) for i in xref])
if xref:
    i=xref[0]
    for j in range(i-2, min(len(insns),i+60)):
        ins=insns[j]
        note=" <===0xe00" if "0xe00" in ins.op_str else ""
        print("0x%x: %s %s%s"%(ins.address,ins.mnemonic,ins.op_str,note))
