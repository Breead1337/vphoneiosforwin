import struct

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

table_va = 0xfffffe0008c195cc
ec_15_va = table_va + 0x15 * 4

for sname, vm, sz, fo in segs:
    if vm <= ec_15_va < vm + sz:
        kc.seek(fo + (ec_15_va - vm))
        offset = struct.unpack('<i', kc.read(4))[0]
        target = 0xfffffe0008c18c50 + offset
        print(f"Jump table entry for EC 0x15 (SVC): offset {offset:#x} -> target {target:#x}")
        break
