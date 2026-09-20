import struct

with open('/mnt/d/vphonewin/fw/cloud/raw/dyld.bin', 'rb') as f:
    data = f.read()

offset = 32
ncmds, sizeofcmds = struct.unpack_from("<II", data, 16)
for _ in range(ncmds):
    cmd, cmdsize = struct.unpack_from("<II", data, offset)
    if cmd == 0x19:
        segname = data[offset+8:offset+24].split(b'\0')[0].decode('ascii', errors='ignore')
        vmaddr, vmsize, fileoff, filesize = struct.unpack_from("<QQQQ", data, offset+24)
        print(f"Segment {segname:16s}: vmaddr=0x{vmaddr:x} vmsize=0x{vmsize:x} fileoff=0x{fileoff:x} filesize=0x{filesize:x}")
    offset += cmdsize
