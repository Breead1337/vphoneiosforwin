import struct

kc = open('/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin', 'rb')
data = kc.read()

pos = 0
while True:
    pos = data.find(b"initproc\x00", pos)
    if pos == -1: break
    print(f"Found 'initproc\\0' at file offset {pos:#x}")
    pos += 1
