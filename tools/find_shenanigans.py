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

shen_addr = None
for sname, vm, sz, fo in segs:
    kc.seek(fo)
    data = kc.read(sz)
    idx = data.find(b'shenanigans!')
    if idx != -1:
        shen_addr = vm + idx
        print(f'Found shenanigans! string at {shen_addr:#x} in {sname}')
        break

if shen_addr:
    md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)
    for sname, vm, sz, fo in segs:
        if sname == '__TEXT_EXEC':
            kc.seek(fo)
            code = kc.read(sz)
            for i in range(0, sz, 4):
                insn = struct.unpack_from('<I', code, i)[0]
                if (insn & 0xffffffe0) == 0x52826f60: # mov w..., #0x137b
                    va = vm + i
                    print(f'Found mov ..., #0x137b at {va:#x}:')
                    snip = code[max(0, i-32):min(len(code), i+48)]
                    for ins in md.disasm(snip, va - 32):
                        print(f'  {ins.address:#x}: {ins.mnemonic} {ins.op_str}')
