import sys
KC="/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin"
f=open(KC,"rb").read(); BASE=0xfffffe0007004000
for va in [0xfffffe0007043875,0xfffffe00070438e1,0xfffffe000704380f]:
    o=va-BASE; s=f[o:o+60].split(b"\0")[0]
    print(hex(va),repr(s))
