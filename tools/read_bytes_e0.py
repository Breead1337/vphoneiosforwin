with open('/mnt/d/vphonewin/fw/cloud/raw/dyld.bin', 'rb') as f:
    f.seek(0xe0bd0)
    b = f.read(64)
print("Bytes at 0xe0bd0 in dyld.bin:", b.hex())
