with open('/home/ard/vrwork/us.log', 'r', errors='ignore') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
svc_blocks = []
for i in range(342690, len(lines)):
    if 'Taking exception 2 [SVC]' in lines[i]:
        block = lines[i:i+8]
        svc_blocks.append((i, "".join(block)))

print(f"Total SVCs after line 342690: {len(svc_blocks)}")
for line_no, blk in svc_blocks:
    print(f"--- Line {line_no} ---")
    print(blk.strip())
