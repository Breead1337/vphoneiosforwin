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

    # Look for caller of 0xfffffe0008ad55f0 (the putc dispatcher)
    # Earlier we saw:
    # Match at 0xfffffe0008aafde8: adrp x16, #0xfffffe0008ad5000; add x16, x16, #0x5f0
    # Match at 0xfffffe000927ca9c: adrp x16, #0xfffffe0008ad5000; add x16, x16, #0x5f0
    # Match at 0xfffffe0008ad5664: adrp x16, #0xfffffe0008ad5000; add x16, x16, #0x5f0
    print("Callers of 0xfffffe0008ad55f0 are around 0xfffffe0008aafde8 and 0xfffffe000927ca9c")
