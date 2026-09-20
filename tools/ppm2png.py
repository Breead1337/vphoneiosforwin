import struct
import zlib
import sys

def ppm_to_png(ppm_path, png_path):
    with open(ppm_path, 'rb') as f:
        magic = f.readline().strip()
        dims = f.readline().strip().split()
        maxv = f.readline().strip()
        w, h = int(dims[0]), int(dims[1])
        raw = f.read()

    raw_lines = []
    line_bytes = w * 3
    for y in range(h):
        raw_lines.append(b'\x00' + raw[y*line_bytes:(y+1)*line_bytes])
    raw_data = b''.join(raw_lines)
    comp = zlib.compress(raw_data, 9)

    def chunk(tag, data):
        crc = zlib.crc32(tag + data) & 0xffffffff
        return struct.pack('>I', len(data)) + tag + data + struct.pack('>I', crc)

    png = b'\x89PNG\r\n\x1a\n'
    ihdr = struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0)
    png += chunk(b'IHDR', ihdr)
    png += chunk(b'IDAT', comp)
    png += chunk(b'IEND', b'')

    with open(png_path, 'wb') as f:
        f.write(png)
    print(f'Successfully wrote {png_path} ({w}x{h})')

if __name__ == '__main__':
    src = sys.argv[1] if len(sys.argv) > 1 else '/home/ard/vrwork/framebuffer.ppm'
    dst = sys.argv[2] if len(sys.argv) > 2 else '/mnt/d/vphonewin/_work/screenshot.png'
    ppm_to_png(src, dst)
