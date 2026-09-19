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

def find_str(s):
    for sname, vm, sz, fo in segs:
        kc.seek(fo)
        data = kc.read(sz)
        idx = data.find(s)
        if idx != -1:
            print(f"Found {s} at {vm+idx:#x} in {sname}")
            return vm + idx
    return None

find_str(b'SEP Boot Failure: status check 1 failed')
find_str(b'AppleSEPBooter.cpp')
