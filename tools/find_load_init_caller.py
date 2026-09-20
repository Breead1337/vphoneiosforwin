import struct, capstone

kc = open('/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin', 'rb')
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

target = 0xfffffe0008f77aac
for sname, vm, sz, fo in segs:
    if 'EXEC' in sname:
        kc.seek(fo)
        data = kc.read(sz)
        for i in range(0, sz - 4, 4):
            w = struct.unpack_from('<I', data, i)[0]
            if (w & 0xfc000000) == 0x94000000: # BL
                imm = w & 0x03ffffff
                if imm & 0x02000000: imm -= 0x04000000
                dest = vm + i + (imm << 2)
                if dest == target:
                    print(f"BL to load_init_program from {vm+i:#x} in {sname}")
