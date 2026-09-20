import sys
import os

def search_file(path, patterns):
    if not os.path.exists(path):
        print("File not found:", path)
        return
    print(f"\n--- Searching {path} ({os.path.getsize(path)} bytes) ---")
    with open(path, "rb") as f:
        data = f.read()

    for p in patterns:
        idx = 0
        found = False
        while True:
            idx = data.find(p, idx)
            if idx == -1:
                break
            found = True
            print(f"Found '{p.decode('utf-8', errors='ignore')}' at file offset 0x{idx:x}")
            idx += len(p)
        if not found:
            print(f"NOT found: '{p.decode('utf-8', errors='ignore')}'")

def main():
    patterns = [
        b"unsuitable CT policy",
        b"code signature validation failed",
        b"is adhoc signed",
        b"CodeSignature: selector:",
        b"unsuitable CT policy %d",
        b"CT policy",
        b"adhoc signed",
        b"rejecting signature"
    ]

    search_file("/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin", patterns)

if __name__ == "__main__":
    main()
