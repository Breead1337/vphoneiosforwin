with open('/mnt/d/vphonewin/fw/cloud/raw/dyld.bin', 'rb') as f:
    f.seek(0xb4584)
    data = f.read(64)
    print("String at 0x700b4584:", repr(data.split(b'\x00')[0]))
