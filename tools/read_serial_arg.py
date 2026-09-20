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

    def read_str(va):
        for sname, vm, sz, fo in segs:
            if vm <= va < vm + sz:
                kc.seek(fo + (va - vm))
                b = bytearray()
                while True:
                    c = kc.read(1)
                    if not c or c == b'\0':
                        break
                    b.extend(c)
                return b.decode('latin1', errors='replace')
        return None

    print("String at 0xfffffe000708cac9:", read_str(0xfffffe000708cac9))
    print("String at 0xfffffe000708cac0:", read_str(0xfffffe000708cac0))
