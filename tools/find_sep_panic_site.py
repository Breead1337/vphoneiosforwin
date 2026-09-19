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

for sname, vm, sz, fo in segs:
    if sname == '__TEXT_EXEC':
        kc.seek(fo)
        code = kc.read(sz)
        md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)
        # Search for mov w..., #0x164
        # 0x164 is 0x52802c80 + rd
        for i in range(0, sz, 4):
            insn = struct.unpack_from('<I', code, i)[0]
            if (insn & 0xffffffe0) == 0x52802c80: # mov w..., #0x164
                va = vm + i
                print(f"Found mov w..., #0x164 at {va:#x}:")
                snip = code[max(0, i-64):min(len(code), i+80)]
                for ins in md.disasm(snip, max(vm, va - 64)):
                    print(f"  {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")
