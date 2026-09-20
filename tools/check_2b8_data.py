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
            if vmaddr <= 0xfffffe000779a2b8 < vmaddr + vmsize:
                print(f"0xfffffe000779a2b8 is in {segname}: vm={vmaddr:#x} sz={vmsize:#x} fo={fileoff:#x}")
                kc.seek(fileoff + (0xfffffe000779a2b8 - vmaddr))
                val = kc.read(32)
                print(f"Data: {val.hex()}")
        off += cmdsize
