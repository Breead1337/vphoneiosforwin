# Search in root2.img or aux.test or any file in /home/ard/vrwork for the bytes around 0x1defd248
import os

needle = None
# In us.log:
# ...with ELR_GL 0xfffffe001defd248
# Let's search if any file contains matches for this address or if we can dump guest memory around it
print("Checking files in /home/ard/vrwork...")
for fname in os.listdir('/home/ard/vrwork'):
    fpath = os.path.join('/home/ard/vrwork', fname)
    if os.path.isfile(fpath):
        sz = os.path.getsize(fpath)
        print(f"  {fname}: {sz} bytes")
