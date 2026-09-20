import os

# Search for SpringBoard or backboardd in root2.img or inspect if it's PCC or iOS
with open('/home/ard/vrwork/root2.img', 'rb') as f:
    # Read chunks
    chunk_sz = 10 * 1024 * 1024
    found = {}
    for i in range(20): # first 200MB
        chunk = f.read(chunk_sz)
        if not chunk:
            break
        for target in [b"SpringBoard", b"backboardd", b"AppleParavirtualizedGraphics", b"IOGPU"]:
            if target in chunk and target not in found:
                found[target] = True
                print(f"Found {target.decode()} in root2.img at chunk {i} (~{i*10}MB)")

print("Search complete. Found:", list(found.keys()))
