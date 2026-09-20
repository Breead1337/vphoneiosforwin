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
base_va = 0xfffffe0008c18c50

for sname, vm, sz, fo in segs:
    if vm <= table_va < vm + sz:
        kc.seek(fo + (table_va - vm))
        entries = struct.unpack('<64i', kc.read(256))
        for ec in range(64):
            dest = base_va + entries[ec]
            if ec in (0x11, 0x12, 0x15, 0x16, 0x20, 0x24, 0x25):
                print(f"EC {ec:#04x}: offset={entries[ec]:#x} -> target={dest:#x}")
        break
