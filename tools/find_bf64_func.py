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
            segs.append((segname, vmaddr, vmsize, fileoff, filesize))
        off += cmdsize

    for segname, vmaddr, vmsize, fileoff, filesize in segs:
        if vmaddr <= 0xfffffe000927bf64 < vmaddr + vmsize:
            kc.seek(fileoff + (0xfffffe000927bf64 - 0x200 - vmaddr))
            code = kc.read(0x300)
            md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)
            func_start = None
            for ins in md.disasm(code, 0xfffffe000927bf64 - 0x200):
                if ins.mnemonic == 'pacibsp':
                    func_start = ins.address
                if ins.address == 0xfffffe000927bf64:
                    break
            print(f"Function start for 0x927bf64 is at: {func_start:#x}")
            break
