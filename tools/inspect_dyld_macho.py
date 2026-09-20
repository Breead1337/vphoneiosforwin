import struct

f = open('/mnt/d/vphonewin/_work/dyld', 'rb')
hdr = f.read(0x1000)
magic, cputype, cpusubtype, filetype, ncmds, sizeofcmds, flags, reserved = struct.unpack_from('<IIIIIIII', hdr, 0)
print(f"dyld magic={magic:#x} filetype={filetype:#x} ncmds={ncmds} flags={flags:#x}")

off = 32
for _ in range(ncmds):
    cmd, cmdsize = struct.unpack_from('<II', hdr, off)
    if cmd == 0x19: # LC_SEGMENT_64
        segname = hdr[off+8:off+24].rstrip(b'\x00').decode('latin1')
        vmaddr, vmsize, fileoff, filesize = struct.unpack_from('<QQQQ', hdr, off+24)
        print(f"  Segment {segname:16s}: vmaddr={vmaddr:#x} vmsize={vmsize:#x} fileoff={fileoff:#x}")
    elif cmd == 0x28 or cmd == 0x80000028: # LC_MAIN or LC_UNIXTHREAD
        print(f"  Thread/Main command {cmd:#x}")
    off += cmdsize
