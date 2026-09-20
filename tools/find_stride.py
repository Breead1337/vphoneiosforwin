with open('/home/ard/vrwork/framebuffer.ppm', 'rb') as f:
    f.readline()
    dims = f.readline().strip().split()
    f.readline()
    raw = f.read()

w = int(dims[0])
h = int(dims[1])
row_bytes = w * 3

print(f"Image: {w}x{h}, data len={len(raw)}")

# Look at rows 100 to 120
for y in range(100, 115):
    # find positions where pixel is bright/white or red
    indices = []
    for x in range(w):
        idx = y * row_bytes + x * 3
        r, g, b = raw[idx], raw[idx+1], raw[idx+2]
        if r > 100 or g > 100 or b > 100:
            indices.append(x)
    if indices:
        print(f"Row {y:3d}: first={indices[0]:4d}, step={indices[1]-indices[0] if len(indices)>1 else 0}, count={len(indices)}")

# Let's find the horizontal offset difference between row 100 and row 101
r100 = [x for x in range(w) if raw[100 * row_bytes + x * 3] > 100]
r101 = [x for x in range(w) if raw[101 * row_bytes + x * 3] > 100]
if r100 and r101:
    shift = r101[0] - r100[0]
    print(f"Shift per row: {shift}")
    # Real row pitch = w - shift, or w + shift
    print(f"Candidate true width/pitch: {w - shift} or {w + shift}")
