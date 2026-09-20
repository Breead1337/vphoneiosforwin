import struct

kc_path = '/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin'
with open(kc_path, 'rb') as kc:
    hdr = kc.read(0x4000)
    ncmds = struct.unpack_from('<I', hdr, 16)[0]
    off = 32
    for _ in range(ncmds):
        cmd, cmdsize = struct.unpack_from('<II', hdr, off)
        if cmd == 0x80000028: # LC_MAIN or LC_UNIXTHREAD
            print(f"LC_MAIN/UNIXTHREAD at {off:#x} sz={cmdsize:#x}")
        elif cmd == 5: # LC_UNIXTHREAD
            # On ARM64: flavor in off+8, count in off+12, state in off+16
            # PC is at off + 16 + 32*8 = off + 16 + 256 = off + 272
            pc = struct.unpack_from('<Q', hdr, off + 272)[0]
            print(f"LC_UNIXTHREAD entry PC = {pc:#x}")
        off += cmdsize
