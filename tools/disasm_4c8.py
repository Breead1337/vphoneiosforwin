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
target = 0xfffffe0008a5f400
for sname, vm, sz, fo in segs:
    if vm <= target < vm + sz:
        kc.seek(fo + (target - vm))
        code = kc.read(0x80)
        for i in range(0, 0x80, 4):
            chunk = code[i:i+4]
            dis = list(md.disasm(chunk, target + i))
            if dis:
                print(f"{target+i:#x}: {chunk.hex()}  {dis[0].mnemonic:8s} {dis[0].op_str}")
            else:
                print(f"{target+i:#x}: {chunk.hex()}  <unknown/data>")
        break
