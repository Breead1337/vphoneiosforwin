kc_path = "/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin"
with open(kc_path, "rb") as f:
    data = f.read()

def va2off(va):
    return va - 0xfffffe0007004000

for va in [0xfffffe00071f8498, 0xfffffe00071f81ec, 0xfffffe00071f7cff, 0xfffffe00071f7d28, 0xfffffe00071f8a96, 0xfffffe00071f8c9d, 0xfffffe00071f7d32, 0xfffffe00071f7d64]:
    fo = va2off(va)
    print(f"0x{va:x}: {repr(data[fo:fo+80].split(b'\\x00')[0])}")
