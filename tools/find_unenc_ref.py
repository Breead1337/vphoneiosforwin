import struct
KC="/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin"
f=open(KC,"rb").read(); BASE=0xfffffe0007004000
STR=0xfffffe0007634920; PAGE=STR & ~0xfff; OFF=STR & 0xfff  # 0x920
def adrp_target(word, pc):
    if (word & 0x9f000000)!=0x90000000: return None
    immlo=(word>>29)&3; immhi=(word>>5)&0x7ffff
    imm=((immhi<<2)|immlo)
    if imm & (1<<20): imm-=(1<<21)
    return (pc & ~0xfff) + (imm<<12)
# scan whole KC __text-ish (search everywhere, filter by add #OFF + preceding adrp to PAGE)
hits=[]
for off in range(0,len(f)-4,4):
    w=struct.unpack_from("<I",f,off)[0]
    # add xR,xR,#OFF (64-bit ADD imm, no shift): 0x91000000 | (OFF<<10) | (Rn<<5)|Rd, Rn==Rd
    if (w & 0xffc00000)==0x91000000:
        imm12=(w>>10)&0xfff
        if imm12==OFF:
            rd=w&0x1f; rn=(w>>5)&0x1f
            if rd==rn:
                va=BASE+off
                # check a few preceding words for adrp to PAGE with same reg
                for back in range(1,6):
                    pw=struct.unpack_from("<I",f,off-back*4)[0]
                    tgt=adrp_target(pw, va-back*4)
                    if tgt==PAGE and (pw&0x1f)==rd:
                        hits.append(va); break
print("refs to 'unencrypted data volume' string (add #0x920 + adrp 0x7634000):")
for h in hits: print("  0x%x"%h)
print("count:",len(hits))
