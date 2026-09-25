import struct
KC="/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin"
f=open(KC,"rb").read()
ncmds=struct.unpack_from("<I",f,16)[0]; o=32
for i in range(ncmds):
    cmd,csz=struct.unpack_from("<II",f,o)
    if cmd==0x19:
        seg=f[o+8:o+24].split(b"\0")[0].decode()
        vmaddr,vmsize,fo2,fsz=struct.unpack_from("<QQQQ",f,o+24)
        if 'TEXT' in seg or 'text' in seg.lower():
            print("%-16s vm=0x%x sz=0x%x foff=0x%x"%(seg,vmaddr,vmsize,fo2))
    o+=csz
