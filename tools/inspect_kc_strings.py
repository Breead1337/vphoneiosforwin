d = open(r"D:\vphonewin\fw\cloud\raw\LLB.vresearch101.RELEASE.bin", "rb").read()

start = 0xa5400
end = 0xa6500
chunk = d[start:end]

# print all null-terminated strings in this chunk
cur = 0
for part in chunk.split(b'\x00'):
    if len(part) >= 2:
        try:
            s = part.decode('ascii')
            print(f"  +{hex(start + cur)}: {s}")
        except:
            pass
    cur += len(part) + 1
