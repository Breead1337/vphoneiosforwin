import struct, capstone

with open('/home/ard/vrwork/launchd', 'rb') as f:
    hdr = f.read(0x2000)
    ncmds = struct.unpack_from('<I', hdr, 16)[0]
    off = 32
    stubs_addr = 0
    stubs_size = 0
    stubs_fileoff = 0
    for _ in range(ncmds):
        cmd, cmdsize = struct.unpack_from('<II', hdr, off)
        if cmd == 0x19:
            nsects = struct.unpack_from('<I', hdr, off+64)[0]
            soff = off + 72
            for _ in range(nsects):
                sname = hdr[soff:soff+16].rstrip(b'\x00').decode('latin1')
                if sname == '__stubs':
                    stubs_addr, stubs_size, stubs_fileoff = struct.unpack_from('<QQI', hdr, soff+32)
                    print(f'__stubs: addr={hex(stubs_addr)} size={hex(stubs_size)} fileoff={hex(stubs_fileoff)}')
                soff += 80
        off += cmdsize

# 0x100058580 is inside __stubs!
# Each stub is 12 or 16 bytes. Let's see what stub 0x100058580 is!
with open('/home/ard/vrwork/launchd', 'rb') as f:
    f.seek(stubs_fileoff + (0x100058580 - stubs_addr))
    code = f.read(32)
    md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)
    print('Stub at 0x100058580:')
    for ins in md.disasm(code, 0x100058580):
        print(f'  0x{ins.address:08x}: {ins.mnemonic} {ins.op_str}')
