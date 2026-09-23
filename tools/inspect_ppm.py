import struct
import zlib
from PIL import Image

def save_png(pixels, w, h, out_path):
    im = Image.new("RGB", (w, h))
    im.putdata(pixels)
    im.save(out_path)
    print(f"Saved {out_path}")

def main():
    ppm_path = "/home/ard/vrwork/framebuffer.ppm"
    with open(ppm_path, "rb") as f:
        magic = f.readline().strip()
        dims = f.readline().strip().split()
        maxv = f.readline().strip()
        w, h = int(dims[0]), int(dims[1])
        raw = f.read()

    print(f"PPM: {w}x{h}, raw bytes: {len(raw)}")
    
    # Analyze pixels
    rgb_list = []
    for i in range(0, len(raw), 3):
        rgb_list.append((raw[i], raw[i+1], raw[i+2]))
        
    save_png(rgb_list, w, h, "/mnt/d/vphonewin/_work/ppm_as_is.png")

if __name__ == '__main__':
    main()
