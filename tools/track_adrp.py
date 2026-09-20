import struct, capstone

kc = open('fw/cloud/raw/kernelcache.research.vresearch101.bin', 'rb')
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

targets = {0xfffffe0007201136, 0xfffffe0007201172, 0xfffffe000708cac9}

md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)
md.detail = True

for sname, vm, sz, fo in segs:
    if 'TEXT' in sname:
        kc.seek(fo)
        code = kc.read(sz)
        regs = {}
        for ins in md.disasm(code, vm):
            if ins.mnemonic == 'adrp':
                rd = ins.operands[0].reg
                imm = ins.operands[1].imm
                regs[rd] = imm
            elif ins.mnemonic == 'add' and len(ins.operands) >= 3:
                rn = ins.operands[1].reg
                if rn in regs and ins.operands[2].type == capstone.arm64.ARM64_OP_IMM:
                    val = regs[rn] + ins.operands[2].imm
                    if val in targets:
                        print(f"Found ref to {val:#x} at {ins.address:#x} in {sname}: {ins.mnemonic} {ins.op_str}")
                # if rd is overwritten, remove from regs
                rd = ins.operands[0].reg
                if rd in regs and rd != rn:
                    del regs[rd]
            elif len(ins.operands) > 0 and ins.operands[0].type == capstone.arm64.ARM64_OP_REG:
                rd = ins.operands[0].reg
                if rd in regs:
                    del regs[rd]
