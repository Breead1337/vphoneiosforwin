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

    print("Kernelcache segments:")
    for sname, vm, sz, fo in segs:
        print(f"  {sname:20s}: {vm:#018x} .. {vm+sz:#018x} (size {sz:#x})")
        if vm <= 0xfffffe001defd000 < vm + sz:
            print(f"    *** 0xfffffe001defd000 is inside {sname}! ***")
