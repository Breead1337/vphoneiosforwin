#!/usr/bin/env python3
import struct
def b(src,tgt):
    off=(tgt-src)//4
    instr=0x14000000|(off & 0x03ffffff)
    return struct.pack('<I',instr).hex()
def bcond(src,tgt,cond):  # cond NE=1
    off=(tgt-src)//4
    instr=0x54000000|((off & 0x7ffff)<<5)|cond
    return struct.pack('<I',instr).hex()
CAVE=0x51a8
# stub layout
i0=CAVE      # stp
i5=CAVE+0x14 # b.ne @ offset 0x14 (6th instr: stp,mov,svc,cmp,ldp,bne)
i7=CAVE+0x1c # b   @ offset 0x1c (8th instr)
print("0x63c94 -> b 0x51a8   :", b(0x63c94, CAVE))
print("stub b.ne@0x%x -> 0x62c10:"%i5, bcond(i5,0x62c10,1))
print("stub b   @0x%x -> 0x63c98:"%i7, b(i7,0x63c98))
# assemble full stub
parts=["e007bfa9","900280d2","011000d4","1f0400f1","e007c1a8",
       bcond(i5,0x62c10,1),"7f2303d5",b(i7,0x63c98)]
print("STUB=","".join(parts))
