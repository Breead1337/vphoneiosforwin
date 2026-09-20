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

    # Look for any function that writes to [0xfffffe000779a0d0]
    # We can scan for ADRP to 0x779a000 followed by STR xN, [xM, #0xd0]
    print("Searching for writes to 0x779a0d0 (dt_base)...")
    for sname, vm, sz, fo in segs:
        if 'TEXT' in sname:
            kc.seek(fo)
            data = kc.read(sz)
            for i in range(0, len(data) - 4, 4):
                word1 = struct.unpack_from('<I', data, i)[0]
                pc = vm + i
                # str xN, [xM, #0xd0]:
                # size=11 (64-bit), 11100100, imm12=0xd0>>3 = 0x1a -> (0x1a << 10)
                # 0xf9000000 | (0x1a << 10) = 0xf9006800
                if (word1 & 0xffc00000) == 0xf9006800:
                    rn = (word1 >> 5) & 0x1f
                    rt = word1 & 0x1f
                    # check previous instruction (pc - 4) for adrp
                    if i >= 4:
                        word0 = struct.unpack_from('<I', data, i - 4)[0]
                        if (word0 >> 26) & 0x1f == 0x10 and (word0 >> 31) == 1: # ADRP
                            immhi = (word0 >> 5) & 0x7ffff
                            immlo = (word0 >> 29) & 3
                            imm = (immhi << 2) | immlo
                            if imm & 0x100000:
                                imm -= 0x200000
                            adrp_page = ((pc - 4) & ~0xfff) + (imm << 12)
                            if adrp_page == 0xfffffe000779a000:
                                print(f"  MATCH: at {pc:#x} ({sname}): str x{rt}, [x{rn}, #0xd0] (after adrp x{rn} to 0x779a000)!")
