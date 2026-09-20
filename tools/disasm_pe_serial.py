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

    targets = [0xfffffe00092d00a0, 0xfffffe00092d49e4, 0xfffffe000927cca4]
    md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)
    for target_va in targets:
        for sname, vm, sz, fo in segs:
            if vm <= target_va < vm + sz:
                kc.seek(fo + (target_va - vm))
                code = kc.read(0x180)
                print(f"\nDisassembly at {target_va:#x} in {sname}:")
                for ins in md.disasm(code, target_va):
                    print(f"  {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")
                break
