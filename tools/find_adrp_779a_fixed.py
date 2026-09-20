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
    md.detail = True
    target = 0xfffffe000779a000

    print(f"Searching for ADRP pointing to {target:#x}...")
    for sname, vm, sz, fo in segs:
        if 'TEXT' in sname:
            kc.seek(fo)
            code = kc.read(sz)
            # Scan in chunks of 1MB
            chunk_sz = 1024 * 1024
            for c_start in range(0, sz, chunk_sz):
                c_code = code[c_start:c_start+chunk_sz]
                c_va = vm + c_start
                for ins in md.disasm(c_code, c_va):
                    if ins.mnemonic == 'adrp':
                        imm = ins.operands[1].imm & 0xffffffffffffffff
                        if imm == target:
                            print(f"  {ins.address:#x} in {sname}: {ins.mnemonic} {ins.op_str}")
