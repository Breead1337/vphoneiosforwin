import sys
import os

files = [
    "/mnt/d/vphonewin/fw/cloud/kernelcache.release.vresearch101",
    "/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin"
]

for fpath in files:
    if os.path.exists(fpath):
        with open(fpath, "rb") as f:
            magic = f.read(16)
        print(f"{fpath}: size={os.path.getsize(fpath)} magic={magic.hex()} ({magic})")
