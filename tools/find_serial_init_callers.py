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

    target = 0xfffffe000927cca4
    print(f"Scanning for BL / B to {target:#x} across all TEXT segments...")
    
    for sname, vm, sz, fo in segs:
        if 'TEXT' in sname:
            kc.seek(fo)
            data = kc.read(sz)
            # Scan every 4 bytes
            for i in range(0, len(data), 4):
                word = struct.unpack_from('<I', data, i)[0]
                pc = vm + i
                # BL opcode: 0x94000000 (bits 31..26 = 0b100101)
                # B opcode:  0x14000000 (bits 31..26 = 0b000101)
                top6 = (word >> 26) & 0x3f
                if top6 in [0b100101, 0b000101]: # BL or B
                    imm26 = word & 0x03ffffff
                    # Sign extend imm26
                    if imm26 & 0x02000000:
                        imm26 -= 0x04000000
                    dest = pc + (imm26 << 2)
                    if dest == target:
                        m = "BL" if top6 == 0b100101 else "B"
                        print(f"  Found {m} to {target:#x} at {pc:#x} in {sname}")
