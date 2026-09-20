import struct

with open('/mnt/d/vphonewin/fw/cloud/raw/dyld.bin', 'rb') as f:
    hdr = f.read(0x10000)

magic, cputype, cpusubtype, filetype, ncmds, sizeofcmds, flags, reserved = struct.unpack('<IIIIIIII', hdr[:32])
print(f"dyld Mach-O: magic={hex(magic)} ncmds={ncmds} flags={hex(flags)}")

off = 32
for i in range(ncmds):
    cmd, cmdsize = struct.unpack_from('<II', hdr, off)
    if cmd == 0x80000028: # LC_MAIN
        entryoff, stacksize = struct.unpack_from('<QQ', hdr, off + 8)
        print(f"LC_MAIN: entryoff={hex(entryoff)} stacksize={hex(stacksize)}")
    elif cmd == 0x5: # LC_UNIXTHREAD
        flavor, count = struct.unpack_from('<II', hdr, off + 8)
        print(f"LC_UNIXTHREAD: flavor={hex(flavor)} count={count}")
        pc = struct.unpack_from('<Q', hdr, off + 16 + 32*8)[0]
        print(f"  Thread PC={hex(pc)}")
    elif cmd == 0x19: # LC_SEGMENT_64
        segname = hdr[off+8:off+24].rstrip(b'\x00').decode('latin1')
        vmaddr, vmsize, fileoff, filesize = struct.unpack_from('<QQQQ', hdr, off+24)
        print(f"  Segment {segname:16s}: vmaddr={hex(vmaddr)} vmsize={hex(vmsize)} fileoff={hex(fileoff)}")
    off += cmdsize
