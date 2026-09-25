import struct, capstone
KC="/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin"
f=open(KC,"rb").read(); BASE=0xfffffe0007004000
TXT_VA=0xfffffe000887aa00; TXT_FOFF=0x1876a00; TXT_SZ=0x147b50
md=capstone.Cs(capstone.CS_ARCH_ARM64,capstone.CS_MODE_LITTLE_ENDIAN); md.detail=True; md.skipdata=True
code=f[TXT_FOFF:TXT_FOFF+TXT_SZ]
hits=[]
for ins in md.disasm(code,TXT_VA):
    for op in ins.operands:
        if op.type==capstone.arm64.ARM64_OP_MEM and op.mem.disp==0xe00:
            hits.append((ins.address,ins.mnemonic,ins.op_str,ins.reg_name(op.mem.base) if op.mem.base else "?"))
print("APFS __text insns with [reg,#0xe00]:",len(hits))
for a,m,o,b in hits:
    print("  0x%x: %s %s  (base %s)"%(a,m,o,b))
