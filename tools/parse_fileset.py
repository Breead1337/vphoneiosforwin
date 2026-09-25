import struct, sys
KC="/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin"
f=open(KC,"rb").read()
ncmds,szcmds=struct.unpack_from("<II",f,16)
o=32; entries=[]
for i in range(ncmds):
    cmd,csz=struct.unpack_from("<II",f,o)
    if cmd==0x80000035:  # LC_FILESET_ENTRY
        vmaddr,fileoff,entryid_off=struct.unpack_from("<QQI",f,o+8)
        name=f[o+entryid_off:o+entryid_off+80].split(b"\0")[0].decode(errors="replace")
        entries.append((vmaddr,fileoff,name))
    o+=csz
print("fileset entries:",len(entries))
for vmaddr,fileoff,name in entries:
    if "apfs" in name.lower() or "keystore" in name.lower() or "AppleKeyStore" in name or "sep" in name.lower():
        print("  %-55s vmaddr=0x%x fileoff=0x%x"%(name,vmaddr,fileoff))
