import struct
KC="/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin"
f=open(KC,"rb").read()
foff=0x6089b0  # apfs kext macho
ncmds=struct.unpack_from("<I",f,foff+16)[0]
o=foff+32
print("APFS kext load cmds:",ncmds)
for i in range(ncmds):
    cmd,csz=struct.unpack_from("<II",f,o)
    if cmd==0x19:
        seg=f[o+8:o+24].split(b"\0")[0].decode()
        vmaddr,vmsize,fo2,fsz=struct.unpack_from("<QQQQ",f,o+24)
        nsec=struct.unpack_from("<I",f,o+64)[0]
        print("SEG %-14s vm=0x%x sz=0x%x foff=0x%x nsec=%d"%(seg,vmaddr,vmsize,fo2,nsec))
        so=o+72
        for s in range(nsec):
            sn=f[so:so+16].split(b"\0")[0].decode()
            sa,ss=struct.unpack_from("<QQ",f,so+32); sfo=struct.unpack_from("<I",f,so+48)[0]
            print("   %-16s va=0x%x sz=0x%x foff=0x%x"%(sn,sa,ss,sfo))
            so+=80
    o+=csz
