import struct, capstone
KC="/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin"
f=open(KC,"rb").read(); BASE=0xfffffe0007004000
md=capstone.Cs(capstone.CS_ARCH_ARM64,capstone.CS_MODE_LITTLE_ENDIAN); md.detail=True
# scan whole file for movz/movk wN,#0xc002 and mov wN,#0xc002-ish
hits=[]
for off in range(0,len(f)-4,4):
    w=struct.unpack_from("<I",f,off)[0]
    # MOVZ Wn,#0xc002 : 0x52800000 | (0xc002<<5) | Rd  (32-bit)
    if (w & 0xffe0001f)==0x52980000 and ((w>>5)&0xffff)==0xc002:
        hits.append((BASE+off,w&0x1f,"movz"))
    # MOVK too
    if (w & 0xffe0001f)==0x72980000 and ((w>>5)&0xffff)==0xc002:
        hits.append((BASE+off,w&0x1f,"movk"))
print("movz/movk #0xc002 sites:",len(hits))
for va,rd,k in hits[:20]:
    # which region?
    reg="main-kernel"
    if va>=0xfffffe000887aa00 and va<0xfffffe00089c2550: reg="APFS __text"
    elif va>=0xfffffe0007230b50 and va<0xfffffe00072360d0: reg="AppleSEPKeyStore"
    print("  0x%x %s w%d  [%s]"%(va,k,rd,reg))
