import struct

kc_path = "/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin"
with open(kc_path, "rb") as f:
    data = f.read()

# Search for "AppleParavirtualized"
pos = 0
while True:
    idx = data.find(b"AppleParavirtualized", pos)
    if idx == -1: break
    print(f"Found at 0x{idx:x}: {repr(data[idx:idx+60].split(b'\\x00')[0])}")
    pos = idx + 20

# Search for "apv-" or "APV"
pos = 0
while True:
    idx = data.find(b"APV-", pos)
    if idx == -1: break
    print(f"Found APV- at 0x{idx:x}: {repr(data[idx:idx+60].split(b'\\x00')[0])}")
    pos = idx + 4
