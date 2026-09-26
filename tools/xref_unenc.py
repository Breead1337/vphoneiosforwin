import capstone
KC="/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin"
f=open(KC,"rb").read(); BASE=0xfffffe0007004000
STR=0xfffffe0007634920  # "unencrypted data volume is not allowed" @%s:%d
TXT_VA=0xfffffe000887aa00; TXT_FOFF=0x1876a00; TXT_SZ=0x147b50
md=capstone.Cs(capstone.CS_ARCH_ARM64,capstone.CS_MODE_LITTLE_ENDIAN); md.detail=True; md.skipdata=True
adrp={}; hits=[]
for ins in md.disasm(f[TXT_FOFF:TXT_FOFF+TXT_SZ],TXT_VA):
    if ins.mnemonic=="adrp":
        try: adrp[ins.reg_name(ins.operands[0].reg)]=ins.operands[1].imm
        except: pass
    elif ins.mnemonic=="add" and len(ins.operands)==3 and ins.operands[2].type==capstone.CS_OP_IMM:
        try:
            bn=ins.reg_name(ins.operands[1].reg)
            if bn in adrp and abs(adrp[bn]+ins.operands[2].imm-STR)<0x20: hits.append(ins.address)
        except: pass
print("xref to 'unencrypted data volume' string in APFS __text:",[hex(h) for h in hits])
