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
    target = 0xfffffe000927cca4
    target_page = target & ~0xfff
    target_off = target & 0xfff

    print(f"Searching for references to {target:#x} (page {target_page:#x}, off {target_off:#x})...")
    for sname, vm, sz, fo in segs:
        if 'TEXT' in sname:
            kc.seek(fo)
            code = kc.read(sz)
            regs = {}
            for ins in md.disasm(code, vm):
                if ins.mnemonic in ['bl', 'b']:
                    if len(ins.operands) > 0 and ins.operands[0].type == capstone.arm64.ARM64_OP_IMM:
                        imm = ins.operands[0].imm
                        if (imm & 0xffffffffffff) == (target & 0xffffffffffff):
                            print(f"  Branch to target from {ins.address:#x} in {sname}: {ins.mnemonic} {ins.op_str}")
                elif ins.mnemonic == 'adrp':
                    rd = ins.operands[0].reg
                    imm = ins.operands[1].imm
                    regs[rd] = imm
                elif ins.mnemonic == 'add' and len(ins.operands) >= 3:
                    rn = ins.operands[1].reg
                    if rn in regs and ins.operands[2].type == capstone.arm64.ARM64_OP_IMM:
                        val = regs[rn] + ins.operands[2].imm
                        if (val & 0xffffffffffff) == (target & 0xffffffffffff):
                            print(f"  ADRP+ADD to target from {ins.address:#x} in {sname}: {ins.mnemonic} {ins.op_str}")
                elif ins.mnemonic == 'adr':
                    imm = ins.operands[1].imm
                    if (imm & 0xffffffffffff) == (target & 0xffffffffffff):
                        print(f"  ADR to target from {ins.address:#x} in {sname}: {ins.mnemonic} {ins.op_str}")
                # clear overwritten reg
                if len(ins.operands) > 0 and ins.operands[0].type == capstone.arm64.ARM64_OP_REG and ins.mnemonic != 'adrp':
                    rd = ins.operands[0].reg
                    if rd in regs:
                        del regs[rd]
