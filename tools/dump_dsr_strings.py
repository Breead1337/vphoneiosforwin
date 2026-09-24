#!/usr/bin/env python3
d=open('/home/ard/vrwork/dyld_hybrid','rb').read()
# dump null-terminated strings in the region 0x8e340..0x8e420
o=0x8e340
end=0x8e420
i=o
while i<end:
    e=d.find(b'\0',i)
    if e<0 or e>end: e=end
    if e>i:
        print("0x%x: %r"%(i, d[i:e]))
    i=e+1
