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
        if 'EXEC' in segname or 'TEXT' in segname:
            kc.seek(fileoff)
            code = kc.read(filesize)
            for i in range(0, len(code), 4):
                word = struct.unpack_from('<I', code, i)[0]
                if (word & 0x9f000000) == 0x90000000:
                    pc = vmaddr + i
                    immlo = (word >> 29) & 3
                    immhi = (word >> 5) & 0x7ffff
                    imm = (immhi << 2) | immlo
                    if imm & (1 << 20):
                        imm -= (1 << 21)
                    target_page = (pc & ~0xfff) + (imm << 12)
                    if target_page == 0xfffffe000779a000:
                        # Check next instruction for offset 0x0e8 or 0xe8
                        if i + 4 < len(code):
                            w2 = struct.unpack_from('<I', code, i+4)[0]
                            # ldr/str imm: size in [31:30], [29:26]=1110, [25:24]=01, [23:22]=00, imm12 in [21:10], Rn in [9:5], Rt in [4:0]
                            # For 32-bit (size=2): imm12 = offset / 4. 0xe8 / 4 = 0x3a = 58
                            # For 64-bit (size=3): imm12 = offset / 8. 0xe8 / 8 = 0x1d = 29
                            chunk = code[i:i+24]
                            for ins in md.disasm(chunk, pc):
                                if '0xe8' in ins.op_str:
                                    print(f"Match at {ins.address:#x} ({segname}): {ins.mnemonic:8s} {ins.op_str}")
