import struct

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

    target_va = 0xfffffe000927cca4
    low48 = target_va & 0xffffffffffff
    print(f"Target low 48 bits: {low48:#x}")
    for sname, vm, sz, fo in segs:
        kc.seek(fo)
        data = kc.read(sz)
        for i in range(0, len(data) - 7, 8):
            val = struct.unpack_from('<Q', data, i)[0]
            if (val & 0xffffffffffff) == low48:
                print(f"Found pointer to {target_va:#x} at {vm+i:#x} ({sname}): {val:#018x}")
