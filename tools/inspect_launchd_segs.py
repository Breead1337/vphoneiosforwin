import struct

with open('/home/ard/vrwork/launchd', 'rb') as f:
    hdr = f.read(0x10000)

magic, cputype, cpusubtype, filetype, ncmds, sizeofcmds, flags, reserved = struct.unpack('<IIIIIIII', hdr[:32])
off = 32
for i in range(ncmds):
    cmd, cmdsize = struct.unpack_from('<II', hdr, off)
    if cmd == 0x19: # LC_SEGMENT_64
        segname = hdr[off+8:off+24].split(b'\0')[0].decode('ascii', errors='ignore')
        vmaddr, vmsize, fileoff, filesize = struct.unpack_from('<QQQQ', hdr, off+24)
        print(f"Segment {segname:16s}: vmaddr=0x{vmaddr:x} vmsize=0x{vmsize:x} fileoff=0x{fileoff:x} filesize=0x{filesize:x}")
    off += cmdsize
