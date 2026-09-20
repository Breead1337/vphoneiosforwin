import struct

kc = open('/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin', 'rb')
data = kc.read()

for va, name in [(0xfffffe00071f7d05, "validation_failed"), (0xfffffe00071f8234, "unsuitable_CT"), (0xfffffe000708d990, "TXM_CodeSignature")]:
    target_bytes = struct.pack('<Q', va)
    pos = 0
    while True:
        pos = data.find(target_bytes, pos)
        if pos == -1: break
        print(f"Pointer to {name} found at file offset {pos:#x}")
        pos += 1
