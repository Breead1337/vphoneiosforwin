import struct

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

for sname, vm, sz, fo in segs:
    kc.seek(fo)
    data = kc.read(sz)
    idx = 0
    while True:
        idx = data.find(b'stdout-path', idx)
        if idx == -1:
            break
        print(f"Found 'stdout-path' at {vm+idx:#x} in {sname}")
        idx += 11
