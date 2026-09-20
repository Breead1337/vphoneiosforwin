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
            segs.append((segname, vmaddr, vmsize, fileoff, filesize))
        off += cmdsize

    def read_str(va):
        for segname, vm, sz, fo, fs in segs:
            if vm <= va < vm + sz:
                kc.seek(fo + (va - vm))
                s = kc.read(128).split(b'\x00')[0].decode('latin1', errors='replace')
                print(f"{va:#x} ({segname}): {s!r}")
                return s
        print(f"{va:#x} not in any segment!")
        return None

    read_str(0xfffffe00070b62b2)
    read_str(0xfffffe00070b6397)
    read_str(0xfffffe00070b6392)
    read_str(0xfffffe00070b5f9a)
    read_str(0xfffffe00070b65ae)
    read_str(0xfffffe000708cac9)
    read_str(0xfffffe00070b60e4)
    read_str(0xfffffe00070b5d74)
    read_str(0xfffffe000704361e)
    read_str(0xfffffe000704350e)
    read_str(0xfffffe000704365e)
