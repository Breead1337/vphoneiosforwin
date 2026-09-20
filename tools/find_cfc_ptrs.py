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

# Check 8-byte pointer references in all segments
target = 0xfffffe0008a60cfc
for sname, vm, sz, fo in segs:
    kc.seek(fo)
    data = kc.read(sz)
    for i in range(0, sz - 8, 8):
        ptr = struct.unpack_from('<Q', data, i)[0]
        if ptr == target:
            print(f"Pointer to {target:#x} at {vm + i:#x} in {sname}")

md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)
# Disassemble 0xfffffe0008a60400..0xfffffe0008a60500
target2 = 0xfffffe0008a60400
for sname, vm, sz, fo in segs:
    if vm <= target2 < vm + sz:
        kc.seek(fo + (target2 - vm))
        code = kc.read(0x100)
        print(f"\nDisassembly at {target2:#x}:")
        for ins in md.disasm(code, target2):
            print(f"  {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")
