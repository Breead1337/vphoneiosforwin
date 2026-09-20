with open('/mnt/d/vphonewin/fw/cloud/raw/dyld.bin', 'rb') as f:
    f.seek(0xccc00)
    raw = f.read(64)
    print("Bytes at 0xccc00 in dyld.bin:", raw.hex())
