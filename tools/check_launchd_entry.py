import struct

with open('/home/ard/vrwork/launchd', 'rb') as f:
    hdr = f.read(0x10000)

magic, cputype, cpusubtype, filetype, ncmds, sizeofcmds, flags, reserved = struct.unpack('<IIIIIIII', hdr[:32])
print(f"Mach-O: magic={hex(magic)} ncmds={ncmds} flags={hex(flags)}")

off = 32
for i in range(ncmds):
    cmd, cmdsize = struct.unpack_from('<II', hdr, off)
    if cmd == 0x80000028: # LC_MAIN
        entryoff, stacksize = struct.unpack_from('<QQ', hdr, off + 8)
        print(f"LC_MAIN: entryoff={hex(entryoff)} (vmaddr={hex(0x100000000 + entryoff)}) stacksize={hex(stacksize)}")
    elif cmd == 0x5: # LC_UNIXTHREAD
        flavor, count = struct.unpack_from('<II', hdr, off + 8)
        print(f"LC_UNIXTHREAD: flavor={hex(flavor)} count={count}")
        # if ARM_THREAD_STATE64
        pc = struct.unpack_from('<Q', hdr, off + 16 + 32*8)[0]
        print(f"  Thread PC={hex(pc)}")
    elif cmd == 0xe: # LC_LOAD_DYLINKER
        nameoff = struct.unpack_from('<I', hdr, off + 8)[0]
        name = hdr[off + nameoff: off + cmdsize].rstrip(b'\x00').decode('latin1')
        print(f"LC_LOAD_DYLINKER: {name}")
    off += cmdsize
