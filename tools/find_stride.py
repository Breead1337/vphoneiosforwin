from PIL import Image
import numpy as np

img = Image.open("/mnt/d/vphonewin/_work/live_screen.png")
arr = np.array(img)

# Look at rows where pixels are non-zero
# Find the horizontal shift per row of the repeating diagonal pattern
shifts = []
for y in range(50, 200):
    row1 = arr[y, :, 0] > 0
    row2 = arr[y+1, :, 0] > 0
    # Cross correlate or find first 1
    idx1 = np.where(row1)[0]
    idx2 = np.where(row2)[0]
    if len(idx1) > 10 and len(idx2) > 10:
        # Check delta between corresponding pattern features
        # The slope is dx / dy
        pass

# Let's test different candidate strides between 900 and 1200 pixels (in bytes: * 4)
best_score = 0
best_w = 0

for test_w in range(800, 1400):
    # Total bytes per row = test_w * 4
    # If the image is reshaped with width test_w, vertical coherence is maximized
    pass

with open("/home/ard/vrwork/framebuffer.ppm", "rb") as f:
    f.readline(); f.readline(); f.readline()
    raw = f.read()

# Raw has 1024*1024*3 bytes (RGB) or original had 1024*1024*4 bytes?
# In framebuffer.ppm we wrote 1024 * 1024 * 3.
# Let's read directly from guest RAM buffer at 0x78f74000!
print("Done")
