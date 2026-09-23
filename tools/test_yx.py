from PIL import Image
import numpy as np
from test_metal_untile import retile_8x8

def untile_morton_yx(raw_flat, w, h, tw, th):
    out = np.zeros((h, w, 3), dtype=np.uint8)
    tiles_x = w // tw
    tiles_y = h // th
    t_pixels = tw * th
    idx = 0
    
    # Morton with Y first, then X:
    offsets = []
    for i in range(t_pixels):
        lx = 0
        ly = 0
        bit = 0
        val = i
        while val > 0:
            if val & 1:
                ly |= (1 << bit)
            if val & 2:
                lx |= (1 << bit)
            val >>= 2
            bit += 1
        offsets.append((lx, ly))

    for ty in range(tiles_y):
        for tx in range(tiles_x):
            for lx, ly in offsets:
                if ty * th + ly < h and tx * tw + lx < w:
                    out[ty * th + ly, tx * tw + lx] = raw_flat[idx]
                idx += 1
    return out

def main():
    img = Image.open("D:/vphonewin/_work/latest_screen.png")
    w, h = img.size
    raw = retile_8x8(img)
    raw_flat = raw.reshape(-1, 3)
    
    out_yx_16 = untile_morton_yx(raw_flat, w, h, 16, 16)
    Image.fromarray(out_yx_16).save("D:/vphonewin/_work/test_untile_yx_16x16.png")
    
    out_yx_8 = untile_morton_yx(raw_flat, w, h, 8, 8)
    Image.fromarray(out_yx_8).save("D:/vphonewin/_work/test_untile_yx_8x8.png")
    print("Saved YX variations!")

if __name__ == '__main__':
    main()
