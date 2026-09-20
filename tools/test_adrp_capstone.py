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

    for sname, vm, sz, fo in segs:
        if vm <= 0xfffffe000927cd54 < vm + sz:
            kc.seek(fo + (0xfffffe000927cd54 - vm))
            raw = kc.read(4)
            insn = struct.unpack('<I', raw)[0]
            md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)
            md.detail = True
            for ins in md.disasm(raw, 0xfffffe000927cd54):
                print(f"Insn at {ins.address:#x}: {ins.mnemonic} {ins.op_str}")
                print(f"  raw bytes: {raw.hex()} (0x{insn:08x})")
                print(f"  num operands: {len(ins.operands)}")
                for i, op in enumerate(ins.operands):
                    print(f"    op[{i}]: type={op.type}, reg={op.reg}, imm={op.imm:#x}")
