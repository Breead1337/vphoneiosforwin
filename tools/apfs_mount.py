import struct, capstone
KC="/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin"
f=open(KC,"rb").read(); BASE=0xfffffe0007004000
def find_str(s):
    o=f.find(s.encode()); return (BASE+o) if o>=0 else None
s1=find_str("setting dev block size"); s2=find_str("handle_mount")
print("setting-dev-block-size str:",hex(s1) if s1 else None)
TXT_VA=0xfffffe000887aa00; TXT_FOFF=0x1876a00; TXT_SZ=0x147b50
md=capstone.Cs(capstone.CS_ARCH_ARM64,capstone.CS_MODE_LITTLE_ENDIAN); md.detail=True
code=f[TXT_FOFF:TXT_FOFF+TXT_SZ]
insns=list(md.disasm(code,TXT_VA))
# index for lookup
idx={ins.address:i for i,ins in enumerate(insns)}
adrp={}; xref=[]
for i,ins in enumerate(insns):
    if ins.mnemonic=="adrp":
        adrp[ins.reg_name(ins.operands[0].reg)]=ins.operands[1].imm
    elif ins.mnemonic=="add" and len(ins.operands)==3 and ins.operands[2].type==capstone.CS_OP_IMM:
        bn=ins.reg_name(ins.operands[1].reg)
        if bn in adrp:
            va=adrp[bn]+ins.operands[2].imm
            if s1 and abs(va-s1)<0x20: xref.append((ins.address,i))
print("xrefs to 'setting dev block size':",[hex(a) for a,_ in xref])
# disassemble ~40 insns AFTER the first xref (where crypto null-deref happens)
if xref:
    a,i=xref[0]
    for j in range(i, min(len(insns),i+55)):
        ins=insns[j]
        note=""
        if ins.mnemonic in ("ldr","str","ldrb","strb","ldp","stp") and "#0xe00" in ins.op_str: note="   <=== +0xe00!"
        if "#0xe00" in ins.op_str: note="   <=== 0xe00"
        print("0x%x: %s %s%s"%(ins.address,ins.mnemonic,ins.op_str,note))
