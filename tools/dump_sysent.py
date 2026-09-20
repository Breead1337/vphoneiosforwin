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

sysent_base = 0xfffffe00077513b0
print(f"sysent table at {sysent_base:#x}:")

for num in [1, 2, 3, 4, 5, 6, 20, 37, 38, 44, 54, 58, 60, 80, 98, 194, 195, 197, 362, 363, 380, 423, 424, 444]:
    entry_va = sysent_base + num * 24
    for sname, vm, sz, fo in segs:
        if vm <= entry_va < vm + sz:
            kc.seek(fo + (entry_va - vm))
            data = kc.read(24)
            sy_call = struct.unpack_from('<Q', data, 0)[0]
            sy_munge = struct.unpack_from('<Q', data, 8)[0]
            sy_return_type, sy_narg, sy_arg_bytes = struct.unpack_from('<ihH', data, 16)
            unpac_call = sy_call & 0x0000ffffffffffff
            # If high bit 47 is set, sign extend
            if unpac_call & 0x800000000000:
                unpac_call |= 0xffff000000000000
            print(f"  Syscall #{num:3d} (0x{num:02x}): fn={unpac_call:#x} (raw {sy_call:#018x}), narg={sy_narg}")
            break
