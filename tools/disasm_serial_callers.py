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

    def disasm_caller(va, count=25):
        for sname, vm, sz, fo in segs:
            if vm <= va < vm + sz:
                kc.seek(fo + (va - 20 - vm))
                code = kc.read((count + 5) * 4)
                md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)
                print(f"\n=== Caller at {va:#x} in {sname} ===")
                for ins in md.disasm(code, va - 20):
                    prefix = "-> " if ins.address == va else "   "
                    print(f"{prefix}{ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")
                break

    for caller_va in [0xfffffe0008a7399c, 0xfffffe0008c10d84, 0xfffffe0008c12c60, 0xfffffe00092c4e9c]:
        disasm_caller(caller_va)
