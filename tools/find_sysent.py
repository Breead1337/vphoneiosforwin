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

# In unix_syscall (0xfffffe00090f0ff0):
# Let's find sysent in __DATA_CONST or __DATA
# Let's search for sysent references around 0xfffffe00090f1050
# In disasm_syscall_dispatch:
# 0xfffffe00090f1050: and w26, w25, #0xffff
# 0xfffffe00090f1054: sub w28, w25, #0xb2
# Let's read from 0xfffffe00090f1064 to 0xfffffe00090f1150
for sname, vm, sz, fo in segs:
    if vm <= 0xfffffe00090f1064 < vm + sz:
        kc.seek(fo + (0xfffffe00090f1064 - vm))
        code = kc.read(200)
        import capstone
        md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)
        for ins in md.disasm(code, 0xfffffe00090f1064):
            print(f"  {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")
        break
