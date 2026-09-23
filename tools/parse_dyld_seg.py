import struct

def parse_macho():
    with open("/mnt/d/vphonewin/_work/dyld", "rb") as f:
        d = f.read()

    magic, cputype, cpusubtype, filetype, ncmds, sizeofcmds, flags, reserved = struct.unpack_from("<IIIIIIII", d, 0)
    print(f"Magic: 0x{magic:x}, ncmds: {ncmds}, flags: 0x{flags:x}")

    off = 32
    for _ in range(ncmds):
        cmd, cmdsize = struct.unpack_from("<II", d, off)
        if cmd == 0x19: # LC_SEGMENT_64
            segname = d[off+8:off+24].split(b"\0")[0].decode()
            vmaddr, vmsize, fileoff, filesize = struct.unpack_from("<QQQQ", d, off+24)
            print(f"Segment {segname:16s} vmaddr: 0x{vmaddr:09x} size: 0x{vmsize:x} fileoff: 0x{fileoff:x} filesize: 0x{filesize:x}")
        off += cmdsize

if __name__ == '__main__':
    parse_macho()
