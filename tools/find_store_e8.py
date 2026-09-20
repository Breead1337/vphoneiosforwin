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

    # Look for STR/STP with offset 0xe8 or 0xd0 or 0xe0
    # In ARM64:
    # str wX, [rN, #0xe8] -> 32-bit store unsigned imm:
    # size=10, 11100100, imm12=0xe8 >> 2 = 0x3a -> (0x3a << 10)
    # str xX, [rN, #0xe8] -> 64-bit store unsigned imm:
    # size=11, 11100100, imm12=0xe8 >> 3 = 0x1d -> (0x1d << 10)
    # stp ... [rN, #0xd0] / #0xe0 / etc.
    print("Searching for STR/STP to offset 0xe8...")
    for sname, vm, sz, fo in segs:
        if 'TEXT' in sname:
            kc.seek(fo)
            data = kc.read(sz)
            for i in range(0, len(data), 4):
                word = struct.unpack_from('<I', data, i)[0]
                pc = vm + i
                # str wX, [rN, #0xe8]:
                # 10 111 0 01 00 imm12(0x3a) rn rt -> 0xb900ea00..
                if (word & 0xffc00000) == (0xb9000000 | (0x3a << 10)):
                    rn = (word >> 5) & 0x1f
                    rt = word & 0x1f
                    print(f"  {pc:#x} ({sname}): str w{rt}, [x{rn}, #0xe8]")
                # str xX, [rN, #0xe8]:
                # 11 111 0 01 00 imm12(0x1d) rn rt -> 0xf9007400
                if (word & 0xffc00000) == (0xf9000000 | (0x1d << 10)):
                    rn = (word >> 5) & 0x1f
                    rt = word & 0x1f
                    print(f"  {pc:#x} ({sname}): str x{rt}, [x{rn}, #0xe8]")
