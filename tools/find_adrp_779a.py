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
            segs.append((segname, vmaddr, vmsize, fileoff))
        off += cmdsize

    md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)
    # Search for all occurrences of 0x779a in any instruction immediate
    # Specifically adrp page 0xfffffe000779a000 (or PC relative)
    print("Searching for any references to 0xfffffe000779a000...")
    for sname, vm, sz, fo in segs:
        if 'TEXT' in sname:
            kc.seek(fo)
            code = kc.read(sz)
            # Find all instructions in this segment
            # ADRP produces a page address. If page == 0xfffffe000779a000:
            for ins in md.disasm(code, vm):
                if ins.mnemonic == 'adrp':
                    # Calculate adrp target
                    # In ARM64: imm is PC-relative
                    # Let's check capstone op_str
                    if '0x779a000' in ins.op_str or '779a' in ins.op_str:
                        print(f"  {ins.address:#x} in {sname}: {ins.mnemonic:8s} {ins.op_str}")
