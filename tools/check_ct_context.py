kc_path = "/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin"
with open(kc_path, "rb") as f:
    data = f.read()

# Let's inspect the context around 0x1f4234
off = 0x1f4234
print("Context around 0x1f4234:")
print(repr(data[off - 64 : off + 128]))

# Also check segment for file offset 0x1f4234
import struct
offset = 32
ncmds, sizeofcmds = struct.unpack_from("<II", data, 16)
for _ in range(ncmds):
    cmd, cmdsize = struct.unpack_from("<II", data, offset)
    if cmd == 0x19:
        segname = data[offset+8:offset+24].split(b'\0')[0].decode('ascii', errors='ignore')
        vmaddr, vmsize, fileoff, filesize = struct.unpack_from("<QQQQ", data, offset+24)
        if fileoff <= off < fileoff + filesize:
            print(f"Offset 0x{off:x} is in segment {segname}, VA = 0x{vmaddr + (off - fileoff):x}")
    offset += cmdsize
