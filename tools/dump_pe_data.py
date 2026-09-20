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

    for segname, vmaddr, vmsize, fileoff, filesize in segs:
        if vmaddr <= 0xfffffe000779a200 < vmaddr + vmsize:
            kc.seek(fileoff + (0xfffffe000779a200 - vmaddr))
            data = kc.read(0x100)
            for i in range(0, len(data), 16):
                row = data[i:i+16]
                hex_str = " ".join(f"{b:02x}" for b in row)
                print(f"{0xfffffe000779a200 + i:#x}: {hex_str}")
