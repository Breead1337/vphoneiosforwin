import struct, capstone
KC="/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin"
f=open(KC,"rb").read()
BASE=0xfffffe0007004000
md=capstone.Cs(capstone.CS_ARCH_ARM64,capstone.CS_MODE_LITTLE_ENDIAN); md.detail=True
# scan whole file for msr vbar_el1, xN => 0xd518c000 | Rt  (word LE)
hits=[]
for off in range(0,len(f)-4,4):
    w=struct.unpack_from("<I",f,off)[0]
    if (w & 0xffffffe0)==0xd518c000:
        hits.append((off,w&0x1f))
print("msr vbar_el1 candidates:",len(hits))
for off,rt in hits[:8]:
    va=BASE+off
    print("  @0x%x (file 0x%x) msr vbar_el1, x%d"%(va,off,rt))
    # disasm 12 insns before to find adrp/add computing xRt
    lo=max(0,off-48)
    adrp={}
    for ins in md.disasm(f[lo:off+4],BASE+lo):
        s=""
        if ins.mnemonic=="adrp":
            adrp[ins.reg_name(ins.operands[0].reg)]=ins.operands[1].imm
        if ins.mnemonic=="add" and len(ins.operands)==3 and ins.operands[2].type==capstone.CS_OP_IMM:
            bn=ins.reg_name(ins.operands[1].reg)
            if bn in adrp: s=" => 0x%x"%(adrp[bn]+ins.operands[2].imm)
        print("     0x%x: %s %s%s"%(ins.address,ins.mnemonic,ins.op_str,s))
