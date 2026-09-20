kc_path = "/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin"
with open(kc_path, "rb") as f:
    data = f.read()

sub = b"no registered daemon port"
idx = data.find(sub)
print("Index of 'no registered daemon port':", hex(idx))
if idx != -1:
    va = 0xfffffe0007008000 + (idx - 0x4000)
    print("VA:", hex(va))
    print("Page:", hex(va & ~0xfff), "Off:", hex(va & 0xfff))
