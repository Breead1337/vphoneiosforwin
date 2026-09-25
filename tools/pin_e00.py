import struct, capstone
KC="/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin"
f=open(KC,"rb").read(); BASE=0xfffffe0007004000
TXT_VA=0xfffffe000887aa00; TXT_FOFF=0x1876a00; TXT_SZ=0x147b50
md=capstone.Cs(capstone.CS_ARCH_ARM64,capstone.CS_MODE_LITTLE_ENDIAN); md.detail=True; md.skipdata=True
CRASH_PC=0xfffffe0031a505e4
LOW=CRASH_PC & 0x3FFF
print("crash low14 =",hex(LOW))
for ins in md.disasm(f[TXT_FOFF:TXT_FOFF+TXT_SZ],TXT_VA):
    for op in ins.operands:
        if op.type==capstone.arm64.ARM64_OP_MEM and op.mem.disp==0xe00:
            if (ins.address & 0x3FFF)==LOW:
                slide=CRASH_PC-ins.address
                print("MATCH 0x%x: %s %s | slide=0x%x (mult0x4000=%s)"%(ins.address,ins.mnemonic,ins.op_str,slide, slide%0x4000==0))
