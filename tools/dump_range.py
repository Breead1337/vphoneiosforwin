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

    data = read_bytes(0xfffffe000779a000, 0x300)
    print("Memory at 0xfffffe000779a000:")
    for i in range(0, len(data), 16):
        words = struct.unpack_from('<IIII', data, i)
        hex_words = " ".join(f"{w:08x}" for w in words)
        ascii_repr = "".join(chr(b) if 32 <= b < 127 else "." for b in data[i:i+16])
        print(f"  +{i:#04x} (0x{0xfffffe000779a000+i:x}): {hex_words}  |{ascii_repr}|")
