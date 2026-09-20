kc_path = "/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin"
with open(kc_path, "rb") as f:
    data = f.read()

sub = b"AMFI: '%s': unsuitable CT policy"
idx = data.find(sub)
print("Index of full string:", hex(idx))

# VA calculation
# __PRELINK_TEXT: vmaddr=0xfffffe0007008000, fileoff=0x4000
va = 0xfffffe0007008000 + (idx - 0x4000)
print("Exact VA of format string:", hex(va))
print("Page:", hex(va & ~0xfff), "Off:", hex(va & 0xfff))
