kc_path = "/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin"
with open(kc_path, "rb") as f:
    data = f.read()

off1 = 0x1f4000 + 0x234
print("String at 0x234:", data[off1:off1+80])

off2 = 0x1f4000 + 0xe2d
print("String at 0xe2d:", data[off2:off2+80])
