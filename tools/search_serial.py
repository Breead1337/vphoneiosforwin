import struct, capstone

kc = open('fw/cloud/raw/kernelcache.research.vresearch101.bin', 'rb')
hdr = kc.read(0x4000)
ncmds = struct.unpack_from('<I', hdr, 16)[0]
off = 32
segs = []
for _ in range(ncmds):
    cmd, cmdsize = struct.unpack_from('<II', hdr, off)
    if cmd == 0x19:
        segname = hdr[off+8:off+24].rstrip(b'\x00').decode('latin1')
        vmaddr, vmsize, fileoff, filesize = struct.unpack_from('<QQQQ', hdr, off+24)
        segs.append((segname, vmaddr, vmsize, fileoff))
    off += cmdsize

def search_str(s):
    res = []
    for sname, vm, sz, fo in segs:
        kc.seek(fo)
        data = kc.read(sz)
        idx = 0
        while True:
            idx = data.find(s, idx)
            if idx == -1:
                break
            res.append((vm + idx, sname))
            idx += len(s)
    return res

print("Matches for 'serial':", search_str(b"serial\0"))
print("Matches for 'serial=':", search_str(b"serial="))
print("Matches for 'debug=':", search_str(b"debug="))
print("Matches for 'console=':", search_str(b"console="))
