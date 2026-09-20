kc_path = "/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin"
with open(kc_path, "rb") as f:
    data = f.read()

# __PRELINK_TEXT: vmaddr=0xfffffe0007008000, fileoff=0x4000
def get_str(va):
    off = 0x4000 + (va - 0xfffffe0007008000)
    return repr(data[off:off+100].split(b'\0')[0])

print("String at 0x71f6156:", get_str(0xfffffe00071f6156))
print("String at 0x71f5b69:", get_str(0xfffffe00071f5b69))
print("String at 0x71f6171:", get_str(0xfffffe00071f6171))
print("String at 0x71f6190:", get_str(0xfffffe00071f6190))
