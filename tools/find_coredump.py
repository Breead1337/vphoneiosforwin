import struct, capstone
KC="/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin"
f=open(KC,"rb").read(); BASE=0xfffffe0007004000
def fs(s):
    o=f.find(s.encode()); return (BASE+o) if o>=0 else None
targets={}
for s in ["Corefile is not yet initialized","Cannot write a coredump","Current Magic"]:
    v=fs(s); targets[v]=s; print("%-34s %s"%(s,hex(v) if v else "NF"))
md=capstone.Cs(capstone.CS_ARCH_ARM64,capstone.CS_MODE_LITTLE_ENDIAN); md.detail=True; md.skipdata=True
# scan whole file, find adrp+add to any target, print addr + nearby function start (pacibsp back-scan)
insns=list(md.disasm(f, BASE))
print("total insns:",len(insns))
adrp={}; hits=[]
for i,ins in enumerate(insns):
    if ins.mnemonic=="adrp":
        try: adrp[ins.reg_name(ins.operands[0].reg)]=ins.operands[1].imm
        except: pass
    elif ins.mnemonic in ("add","ldr") and len(ins.operands)>=2:
        try:
            if ins.mnemonic=="add" and ins.operands[2].type==capstone.CS_OP_IMM:
                bn=ins.reg_name(ins.operands[1].reg)
                if bn in adrp:
                    va=adrp[bn]+ins.operands[2].imm
                    for t in targets:
                        if t and abs(va-t)<0x40: hits.append((ins.address,i,targets[t]))
        except: pass
print("xref hits:",len(hits))
for a,i,s in hits[:8]:
    # back-scan for pacibsp (func entry)
    fe=None
    for j in range(i,max(0,i-400),-1):
        if insns[j].mnemonic in ("pacibsp","paciasp"): fe=insns[j].address; break
    print("  xref@0x%x (%s) func_entry~0x%x"%(a,s[:20],fe or 0))
