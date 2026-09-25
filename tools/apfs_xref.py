import struct, capstone
KC="/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin"
f=open(KC,"rb").read(); BASE=0xfffffe0007004000
def find_str(s):
    o=f.find(s.encode()); return (BASE+o) if o>=0 else None
for t in ["migrate_media_keys_if_needed","handle_mount","media key","keybag","crypto","gigalocker","apfs_vfsop_mount","MediaKey"]:
    va=find_str(t); print("%-32s %s"%(t, hex(va) if va else "NF"))
mmk=find_str("migrate_media_keys_if_needed")
md=capstone.Cs(capstone.CS_ARCH_ARM64,capstone.CS_MODE_LITTLE_ENDIAN); md.detail=True
apfs_foff=0x6089b0
span=0x900000
code=f[apfs_foff:apfs_foff+span]
adrp={}; hits=[]
for ins in md.disasm(code,BASE+apfs_foff):
    if ins.mnemonic=="adrp":
        adrp[ins.reg_name(ins.operands[0].reg)]=ins.operands[1].imm
    elif ins.mnemonic=="add" and len(ins.operands)==3 and ins.operands[2].type==capstone.CS_OP_IMM:
        bn=ins.reg_name(ins.operands[1].reg)
        if bn in adrp and mmk and abs(adrp[bn]+ins.operands[2].imm-mmk)<0x30:
            hits.append(ins.address)
print("mmk str va:",hex(mmk) if mmk else None,"xrefs:",[hex(h) for h in hits[:6]])
