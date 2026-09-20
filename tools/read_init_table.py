import struct

kc_path = '/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin'
with open(kc_path, 'rb') as kc:
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

    def read_ptr(va):
        for sname, vm, sz, fo in segs:
            if vm <= va < vm + sz:
                kc.seek(fo + (va - vm))
                val = struct.unpack('<Q', kc.read(8))[0]
                return val
        return None

    p1 = read_ptr(0xfffffe00095270b0)
    print(f"0xfffffe00095270b0: {p1:#018x} (unpac: {p1 & 0x0000ffffffffffff:#018x})")
