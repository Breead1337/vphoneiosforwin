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

def get_str(addr):
    for sname, vm, sz, fo in segs:
        if vm <= addr < vm + sz:
            kc.seek(fo + (addr - vm))
            s = b''
            for _ in range(128):
                ch = kc.read(1)
                if not ch or ch == b'\x00':
                    break
                s += ch
            return s.decode('latin1', errors='replace')
    return None

for sname, vm, sz, fo in segs:
    if sname == '__TEXT_EXEC':
        kc.seek(fo)
        code = kc.read(sz)
        md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)
        md.detail = True
        start_va = 0xfffffe000885ca80
        end_va   = 0xfffffe000885d100
        start_off = start_va - vm
        end_off = end_va - vm
        subcode = code[start_off:end_off]
        cur_adrp = {}
        for ins in md.disasm(subcode, start_va):
            if ins.mnemonic == 'adrp':
                cur_adrp[ins.operands[0].reg] = ins.operands[1].imm
            elif ins.mnemonic == 'add' and len(ins.operands) >= 3 and ins.operands[1].reg in cur_adrp:
                target = cur_adrp[ins.operands[1].reg] + ins.operands[2].imm
                s = get_str(target)
                if s:
                    print(f'{ins.address:#x}: ref str {target:#x} -> "{s}"')
