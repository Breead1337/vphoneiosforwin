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

    print("Searching for writes to 0x779a2c0 or 0x779a0e8...")
    target_page = 0xfffffe000779a000
    for sname, vm, sz, fo in segs:
        if 'TEXT' in sname:
            kc.seek(fo)
            code = kc.read(sz)
            regs = {}
            for ins in md.disasm(code, vm):
                if ins.mnemonic == 'adrp':
                    rd = ins.operands[0].reg
                    imm = ins.operands[1].imm & 0xffffffffffffffff
                    regs[rd] = imm
                elif ins.mnemonic.startswith('str') or ins.mnemonic.startswith('stp'):
                    for op in ins.operands:
                        if op.type == capstone.arm64.ARM64_OP_MEM:
                            rn = op.mem.base
                            disp = op.mem.disp
                            if rn in regs:
                                addr = regs[rn] + disp
                                if addr in [0xfffffe000779a2c0, 0xfffffe000779a0e8, 0xfffffe000779a0d0, 0xfffffe000779a0e0]:
                                    print(f"  Write to {addr:#x} at {ins.address:#x} in {sname}: {ins.mnemonic} {ins.op_str}")
                elif len(ins.operands) > 0 and ins.operands[0].type == capstone.arm64.ARM64_OP_REG and ins.mnemonic != 'adrp':
                    rd = ins.operands[0].reg
                    if rd in regs:
                        del regs[rd]
