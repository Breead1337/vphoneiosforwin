import struct
import re

kc_path = "/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin"
with open(kc_path, "rb") as f:
    data = f.read()

# Search for plist or prelink info
# The prelink info is in __PRELINK_INFO segment
# Let's find segments
segments = []
offset = 32
ncmds, sizeofcmds = struct.unpack_from("<II", data, 16)
for _ in range(ncmds):
    cmd, cmdsize = struct.unpack_from("<II", data, offset)
    if cmd == 0x19:
        segname = data[offset+8:offset+24].split(b'\0')[0].decode('ascii', errors='ignore')
        vmaddr, vmsize, fileoff, filesize = struct.unpack_from("<QQQQ", data, offset+24)
        if segname == "__PRELINK_INFO":
            info_data = data[fileoff:fileoff+filesize]
            print(f"Found __PRELINK_INFO: {len(info_data)} bytes")
            # Let's find AMFI dictionary or bundle identifier
            # Search for com.apple.driver.AppleMobileFileIntegrity
            idx = info_data.find(b"com.apple.driver.AppleMobileFileIntegrity")
            if idx != -1:
                start = max(0, idx - 500)
                end = min(len(info_data), idx + 2000)
                chunk = info_data[start:end].decode('latin1', errors='ignore')
                print("AMFI Info chunk:")
                print(chunk)
    offset += cmdsize

