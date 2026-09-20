import struct

kc = open('/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin', 'rb')
data = kc.read()

pos = 0
while True:
    pos = data.find(b"/sbin/launchd\x00", pos)
    if pos == -1: break
    print(f"Found '/sbin/launchd' at file offset {pos:#x}")
    pos += 1
