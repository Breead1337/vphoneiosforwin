#!/usr/bin/env python3
# Find an executable code cave (run of >=48 zero bytes) inside dyld's __TEXT segment,
# for a PID-conditional trampoline. Reports file offset (== vmaddr, flat) and size.
import struct
d = open("/home/ard/vrwork/dyld_hybrid","rb").read()
ncmds=struct.unpack_from("<I",d,16)[0]; p=32; textseg=None; sects=[]
for _ in range(ncmds):
    cmd,sz=struct.unpack_from("<II",d,p)
    if cmd==0x19:
        seg=d[p+8:p+24].split(b"\0")[0].decode(); vm,vs,fo,fs=struct.unpack_from("<QQQQ",d,p+24)
        if seg=="__TEXT": textseg=(vm,fo,fs)
        nsects=struct.unpack_from("<I",d,p+64)[0]; spp=p+72
        for _ in range(nsects):
            sn=d[spp:spp+16].split(b"\0")[0].decode(); addr,size=struct.unpack_from("<QQ",d,spp+32); off=struct.unpack_from("<I",d,spp+48)[0]
            if seg=="__TEXT": sects.append((sn,addr,size,off))
            spp+=80
    p+=sz
print("__TEXT seg vm=0x%x foff=0x%x fsize=0x%x"%textseg)
for sn,addr,size,off in sects:
    print("  sect %-16s vm=0x%x foff=0x%x size=0x%x end=0x%x"%(sn,addr,off,size,off+size))
# scan whole __TEXT file range for zero runs
vm,fo,fs=textseg
region=d[fo:fo+fs]
best=[]; i=0
while i<len(region):
    if region[i]==0:
        j=i
        while j<len(region) and region[j]==0: j+=1
        if j-i>=48:
            best.append((fo+i, j-i))
        i=j
    else: i+=1
print("zero caves (>=48B) in __TEXT:")
for off,ln in best[:20]:
    print("  foff=0x%x vm=0x%x len=%d"%(off, off, ln))
