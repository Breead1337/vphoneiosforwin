import struct

with open('/mnt/d/vphonewin/_work/dyld', 'rb') as f:
    hdr = f.read(32)
    magic, cputype, cpusubtype, filetype, ncmds, sizeofcmds, flags, reserved = struct.unpack('<IIIIIIII', hdr)
    print(f"dyld magic={magic:#x} cpu={cputype:#x}/{cpusubtype:#x} filetype={filetype:#x} ncmds={ncmds}")
    off = 32
    for _ in range(ncmds):
        cmd, cmdsize = struct.unpack_from('<II', f.read(8))
        f.seek(f.tell() - 8)
        cmd_data = f.read(cmdsize)
        if cmd == 0x19: # LC_SEGMENT_64
            segname = cmd_data[8:24].rstrip(b'\x00').decode('latin1')
            vmaddr, vmsize, fileoff, filesize = struct.unpack_from('<QQQQ', cmd_data, 24)
            print(f"  Segment {segname:16s}: {vmaddr:#018x} .. {vmaddr+vmsize:#018x} (file off {fileoff:#x}, sz {filesize:#x})")
