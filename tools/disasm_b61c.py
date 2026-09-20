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

    def disasm_range(start_va, length):
        for sname, vm, sz, fo in segs:
            if vm <= start_va < vm + sz:
                kc.seek(fo + (start_va - vm))
                code = kc.read(length)
                md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)
                print(f"Disassembly of {start_va:#x} to {start_va+length:#x} ({sname}):")
                for ins in md.disasm(code, start_va):
                    print(f"  {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")
                break

    disasm_range(0xfffffe000927b61c, 0xf0)
