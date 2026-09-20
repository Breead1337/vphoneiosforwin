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

md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)

for target in [0xfffffe0008c18a88, 0xfffffe0008c18cb0]:
    for sname, vm, sz, fo in segs:
        if vm <= target < vm + sz:
            kc.seek(fo + (target - vm) - 32)
            code = kc.read(160)
            print(f"\nDisassembly around {target:#x} in {sname}:")
            for ins in md.disasm(code, target - 32):
                prefix = "==> " if ins.address == target else "    "
                print(f"{prefix}{ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")
            break
