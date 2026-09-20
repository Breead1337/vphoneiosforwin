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

    def read_str(va):
        for sname, vm, sz, fo in segs:
            if vm <= va < vm + sz:
                kc.seek(fo + (va - vm))
                b = bytearray()
                while True:
                    c = kc.read(1)
                    if not c or c == b'\0':
                        break
                    b.extend(c)
                return b.decode('latin1', errors='replace')
        return None

    str_offsets = [0x2b2, 0x397, 0x392, 0x3d6, 0x3e4, 0x433, 0x485, 0x494, 0x307]
    print("Strings at 0xfffffe00070b6000 + offset:")
    for o in str_offsets:
        va = 0xfffffe00070b6000 + o
        s = read_str(va)
        print(f"  {va:#x} (+{o:#x}): '{s}'")

    # Disassemble 0xfffffe000927b61c and 0xfffffe000927cf00..0xfffffe000927d1a0
    md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)
    for target_va, sz in [(0xfffffe000927b61c, 0x80), (0xfffffe000927cf00, 0x1a0)]:
        for sname, vm, sz_seg, fo in segs:
            if vm <= target_va < vm + sz_seg:
                kc.seek(fo + (target_va - vm))
                code = kc.read(sz)
                print(f"\nDisassembly at {target_va:#x} ({sname}):")
                for ins in md.disasm(code, target_va):
                    print(f"  {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")
                break
