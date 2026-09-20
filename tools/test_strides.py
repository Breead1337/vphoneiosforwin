import struct
import zlib

with open('/home/ard/vrwork/framebuffer.ppm', 'rb') as f:
    f.readline()
    dims = f.readline().strip().split()
    f.readline()
    raw = f.read()

# Try a few different widths / strides
# Total pixels = len(raw) // 3 = 1048576 = 1024 * 1024
total_px = len(raw) // 3

# Test candidate strides
candidates = [
    # standard resolutions & common strides
    1170, 1125, 1080, 1024, 960, 828, 750, 640,
    # from slope analysis: shift was -36 per row -> candidate 1024 - (-36/something)
    1060, 988, 1024 - 18, 1024 + 18, 1024 - 36, 1024 + 36,
]

def save_png_at_width(stride_px, out_name):
    # calculate height
    h = total_px // stride_px
    if h == 0: return
    w = stride_px
    
    raw_lines = []
    line_bytes = w * 3
    for y in range(h):
        raw_lines.append(b'\x00' + raw[y*line_bytes:(y+1)*line_bytes])
    raw_data = b''.join(raw_lines)
    comp = zlib.compress(raw_data, 6)

    def chunk(tag, data):
        crc = zlib.crc32(tag + data) & 0xffffffff
        return struct.pack('>I', len(data)) + tag + data + struct.pack('>I', crc)

    png = b'\x89PNG\r\n\x1a\n'
    ihdr = struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0)
    png += chunk(b'IHDR', ihdr)
    png += chunk(b'IDAT', comp)
    png += chunk(b'IEND', b'')

    with open(out_name, 'wb') as f:
        f.write(png)
    print(f"Saved {out_name}: {w}x{h}")

for c in [1060, 988, 1024, 1080, 1170]:
    save_png_at_width(c, f'/mnt/d/vphonewin/_work/test_{c}.png')
