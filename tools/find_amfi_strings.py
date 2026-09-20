import struct

kc = open('/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin', 'rb')
data = kc.read()

for s in [b"code signature validation failed", b"unsuitable CT policy", b"CodeSignature: selector"]:
    pos = 0
    while True:
        pos = data.find(s, pos)
        if pos == -1: break
        print(f"Found '{s.decode()}' at file offset {pos:#x}")
        pos += 1
