import struct, capstone

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

    # Look at raw bytes at 0xfffffe000779a2e0
    for segname, vmaddr, vmsize, fileoff, filesize in segs:
        if vmaddr <= 0xfffffe000779a2e0 < vmaddr + vmsize:
            kc.seek(fileoff + (0xfffffe000779a2e0 - vmaddr))
            words = struct.unpack('<4Q', kc.read(32))
            for i, w in enumerate(words):
                # PAC pointer format in static kernelcache:
                # Often upper bits contain PAC signature, or lower 48 bits is the VA
                raw_va = w & 0xffffffffffff
                # Or if signed with PACIA:
                print(f"Entry {i*8:#x}: raw={w:#018x} (masked={raw_va:#x})")
