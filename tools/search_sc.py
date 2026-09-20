import struct

kc_path = '/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin'
with open(kc_path, 'rb') as kc:
    data = kc.read()
    print("Searching for 0x1defd in kernelcache...")
    idx = 0
    while True:
        idx = data.find(b'\xfd\xde\xef\x01', idx) # little-endian 0x01efdefd?
        if idx == -1:
            break
        print(f"Found match at offset {idx:#x}")
        idx += 4

    # Search for shared cache base strings
    for s in [b"SHARED_CACHE", b"shared_cache", b"com.apple.launchd"]:
        idx = 0
        while True:
            idx = data.find(s, idx)
            if idx == -1:
                break
            print(f"Found '{s.decode()}' at offset {idx:#x}")
            idx += len(s)
