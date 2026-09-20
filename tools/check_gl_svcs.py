with open('/home/ard/vrwork/us.log', 'r', errors='ignore') as f:
    lines = f.readlines()

gl_svcs = 0
nongl_svcs = 0
for i in range(342690, len(lines)):
    if 'Taking exception 2 [SVC]' in lines[i]:
        # check next 6 lines
        block = "".join(lines[i:i+6])
        if 'ELR_GL' in block:
            gl_svcs += 1
        else:
            nongl_svcs += 1
            print(f"Non-GL SVC at line {i}:")
            print(block.strip())

print(f"\nTotal SVCs after line 342690: GL={gl_svcs}, Non-GL={nongl_svcs}")
