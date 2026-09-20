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

md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)
md.detail = True

for sname, vm, sz, fo in segs:
    if 'TEXT' in sname:
        kc.seek(fo)
        code = kc.read(sz)
        for ins in md.disasm(code, vm):
            if ins.mnemonic == 'adrp':
                target_page = ins.operands[1].imm
                if 0xfffffe00070b5000 <= target_page <= 0xfffffe00070b8000:
                    print(f"ADRP to {target_page:#x} at {ins.address:#x} in {sname}: {ins.op_str}")
                    # print next 10 instructions
                    idx = ins.address - vm
                    snip = code[idx:idx+48]
                    for sub in md.disasm(snip, ins.address):
                        print(f"    {sub.address:#x}: {sub.mnemonic:8s} {sub.op_str}")
                    break
