from PIL import Image
import numpy as np

def retile_8x8(img):
    w, h = img.size
    pixels = np.array(img)
    raw = np.zeros_like(pixels)
    
    tiles_x = w // 8
    tiles_y = h // 8
    idx = 0
    for ty in range(tiles_y):
        for tx in range(tiles_x):
            for i in range(64):
                lx = (i & 1) | ((i >> 1) & 2) | ((i >> 2) & 4)
                ly = ((i >> 1) & 1) | ((i >> 2) & 2) | ((i >> 3) & 4)
                raw.reshape(-1, 3)[idx] = pixels[ty * 8 + ly, tx * 8 + lx]
                idx += 1
    return raw

def untile_morton(raw_flat, w, h, tw, th):
    out = np.zeros((h, w, 3), dtype=np.uint8)
    tiles_x = w // tw
    tiles_y = h // th
    t_pixels = tw * th
    idx = 0
    
    # Precompute Morton offsets for tile
    offsets = []
    for i in range(t_pixels):
        lx = 0
        ly = 0
        bit = 0
        val = i
        while val > 0:
            if val & 1:
                lx |= (1 << bit)
            if val & 2:
                ly |= (1 << bit)
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
    print(f"Original: {w}x{h}")
    
    raw = retile_8x8(img)
    raw_flat = raw.reshape(-1, 3)
    
    # Test 1: 16x16
    out16 = untile_morton(raw_flat, w, h, 16, 16)
    Image.fromarray(out16).save("D:/vphonewin/_work/test_untile_16x16.png")
    print("Saved test_untile_16x16.png")
    
    # Test 2: 32x32
    out32 = untile_morton(raw_flat, w, h, 32, 32)
    Image.fromarray(out32).save("D:/vphonewin/_work/test_untile_32x32.png")
    print("Saved test_untile_32x32.png")
    
    # Test 3: 16x8
    out16x8 = untile_morton(raw_flat, w, h, 16, 8)
    Image.fromarray(out16x8).save("D:/vphonewin/_work/test_untile_16x8.png")
    print("Saved test_untile_16x8.png")
    
    # Test 4: 8x16
    out8x16 = untile_morton(raw_flat, w, h, 8, 16)
    Image.fromarray(out8x16).save("D:/vphonewin/_work/test_untile_8x16.png")
    print("Saved test_untile_8x16.png")

if __name__ == '__main__':
    main()
