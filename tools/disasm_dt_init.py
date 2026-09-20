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

    def disasm_func(va, count=50):
        for sname, vm, sz, fo in segs:
            if vm <= va < vm + sz:
                kc.seek(fo + (va - vm))
                code = kc.read(count * 4)
                md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)
                print(f"\n--- Disassembly at {va:#x} ({sname}) ---")
                for ins in md.disasm(code, va):
                    print(f"  {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")
                break

    # Find DTInit by checking caller or beginning of DTInit
    # DTInit usually takes (void *dt_base, int dt_size)
    # Let's check 0xfffffe0009279000..0xfffffe0009279200
    disasm_func(0xfffffe0009279000, 40)
    disasm_func(0xfffffe0009279100, 40)
