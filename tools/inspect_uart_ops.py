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

    def read_bytes(va, sz):
        for sname, vm, sz_seg, fo in segs:
            if vm <= va < vm + sz_seg:
                kc.seek(fo + (va - vm))
                return kc.read(sz)
        return None

    data = read_bytes(0xfffffe000779a2e0, 0x60)
    print("uart_ops at 0xfffffe000779a2e0:")
    for i in range(0, len(data), 8):
        val = struct.unpack_from('<Q', data, i)[0]
        print(f"  +{i:#x}: {val:#018x}")

    # Also check what's at 0xfffffe000779a0e8
    data2 = read_bytes(0xfffffe000779a0e8, 16)
    w0, w1, w2, w3 = struct.unpack('<IIII', data2)
    print(f"\n0xfffffe000779a0e8: {w0:#x}, {w1:#x}, {w2:#x}, {w3:#x}")
