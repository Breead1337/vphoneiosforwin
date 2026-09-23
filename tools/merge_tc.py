import struct

def merge():
    d1 = open("/mnt/d/vphonewin/_work/tc/os.trst.bin", "rb").read()
    v1, u1, n1 = struct.unpack_from("<I16sI", d1, 0)
    entries1 = [d1[24 + i*24 : 24 + (i+1)*24] for i in range(n1)]

    d2 = open("/home/ard/vrwork/tc_iphone/ios_raw.trst.bin", "rb").read()
    v2, u2, n2 = struct.unpack_from("<I16sI", d2, 0)
    entries2 = [d2[24 + i*24 : 24 + (i+1)*24] for i in range(n2)]

    all_entries = {}
    for e in entries1 + entries2:
        cdhash = e[:20]
        # Keep entry if not present
        if cdhash not in all_entries:
            all_entries[cdhash] = e

    # Sort entries by CDHash as required by XNU bsearch
    sorted_entries = sorted(all_entries.values(), key=lambda e: e[:20])
    out_hdr = struct.pack("<I16sI", 2, u2, len(sorted_entries))
    merged = out_hdr + b"".join(sorted_entries)

    out_path = "/home/ard/vrwork/tc_iphone/merged.trst.bin"
    open(out_path, "wb").write(merged)
    print(f"Merged TC: {n1} from CloudOS + {n2} from iOS -> {len(sorted_entries)} unique entries saved to {out_path} ({len(merged)} bytes)")

if __name__ == "__main__":
    merge()
