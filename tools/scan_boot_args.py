import struct, capstone

kc = open('fw/cloud/raw/kernelcache.research.vresearch101.bin', 'rb')
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

# In start_first_cpu:
# x0 = boot_args
# In __TEXT_BOOT_EXEC:
kc.seek(0x22cc000)
code = kc.read(0x8000)
md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)

print("Scanning __TEXT_BOOT_EXEC for deviceTreeP loads...")
for ins in md.disasm(code, 0xfffffe00092d0000):
    if ins.mnemonic in ['ldr', 'ldp'] and any(f'#{hex(o)}' in ins.op_str for o in range(0x40, 0x70, 8)):
        print(f"  {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")
