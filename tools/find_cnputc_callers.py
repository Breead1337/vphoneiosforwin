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

    md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)
    for segname, vmaddr, vmsize, fileoff, filesize in segs:
        if 'EXEC' in segname:
            kc.seek(fileoff)
            code = kc.read(filesize)
            # Find BL instructions to 0xfffffe0008ad5a9c
            # In ARM64: BL opcode: [31]=1, [30:26]=00101, [25:0]=imm26 (signed word offset)
            target = 0xfffffe0008ad5a9c
            for i in range(0, len(code), 4):
                word = struct.unpack_from('<I', code, i)[0]
                if (word & 0xfc000000) == 0x94000000:
                    imm26 = word & 0x3ffffff
                    if imm26 & (1 << 25):
                        imm26 -= (1 << 26)
                    pc = vmaddr + i
                    dest = pc + imm26 * 4
                    if dest == target:
                        print(f"BL to cnputc at {pc:#x} ({segname})")
                # Also ADRP to page 0xfffffe0008ad5000
                elif (word & 0x9f000000) == 0x90000000:
                    immlo = (word >> 29) & 3
                    immhi = (word >> 5) & 0x7ffff
                    imm = (immhi << 2) | immlo
                    if imm & (1 << 20):
                        imm -= (1 << 21)
                    pc = vmaddr + i
                    target_page = (pc & ~0xfff) + (imm << 12)
                    if target_page == 0xfffffe0008ad5000 and i + 4 < len(code):
                        w2 = struct.unpack_from('<I', code, i+4)[0]
                        # check if add to 0xa9c
                        if (w2 & 0xffc003e0) == 0x912a7000: # add ..., #0xa9c
                            print(f"ADRP+ADD cnputc at {pc:#x} ({segname})")
