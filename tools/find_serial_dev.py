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
            print(f"Seg: {segname:20s} vm={vmaddr:#x} sz={vmsize:#x} fo={fileoff:#x}")
        off += cmdsize

    md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)
    for segname, vmaddr, vmsize, fileoff, filesize in segs:
        if 'EXEC' in segname or 'TEXT' in segname:
            print(f"Scanning {segname} ({filesize} bytes)...")
            kc.seek(fileoff)
            code = kc.read(filesize)
            # Scan for adrp instructions that target page 0xfffffe000949c000
            # ADRP computes: (PC & ~0xfff) + (imm << 12)
            # We can check instructions with capstone or raw binary
            for i in range(0, len(code), 4):
                word = struct.unpack_from('<I', code, i)[0]
                # ADRP opcode pattern: [31]=1, [30:29]=immlo, [28:24]=10000, [23:5]=immhi, [4:0]=Rd
                if (word & 0x9f000000) == 0x90000000:
                    pc = vmaddr + i
                    immlo = (word >> 29) & 3
                    immhi = (word >> 5) & 0x7ffff
                    imm = (immhi << 2) | immlo
                    if imm & (1 << 20):
                        imm -= (1 << 21)
                    target_page = (pc & ~0xfff) + (imm << 12)
                    if target_page == 0xfffffe000949c000:
                        rd = word & 0x1f
                        # disasm next 4 instructions
                        chunk = code[i:i+20]
                        print(f"\nMatch at {pc:#x} in {segname}:")
                        for ins in md.disasm(chunk, pc):
                            print(f"  {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")
