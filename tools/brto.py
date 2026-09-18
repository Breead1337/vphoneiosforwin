# brto.py FILE 0xVA [0xVA...] — find b/bl/b.cond/cbz/tbz branching to VA in a Mach-O's exec segments
import sys, struct
d = open(sys.argv[1], 'rb').read(); T = {int(a, 16) for a in sys.argv[2:]}
n = struct.unpack('<I', d[16:20])[0]; o = 32
def sx(v, b): return v - (1 << b) if v >> (b - 1) else v
while n:
    c, sz = struct.unpack('<II', d[o:o+8]); n -= 1
    if c == 0x19:
        vm, vs, fo, fs, mp, ip = struct.unpack('<QQQQII', d[o+24:o+64])
        if ip & 4:
            for i in range(0, fs, 4):
                w = struct.unpack('<I', d[fo+i:fo+i+4])[0]; pc = vm + i; t = None
                if w >> 26 in (5, 0x25): t = pc + sx(w & 0x3ffffff, 26) * 4
                elif (w & 0xff000010) == 0x54000000 or (w >> 25) & 0x3f == 0x1a: t = pc + sx((w >> 5) & 0x7ffff, 19) * 4
                elif (w >> 25) & 0x3f == 0x1b: t = pc + sx((w >> 5) & 0x3fff, 14) * 4
                if t in T: print(f'{t:#x} <- {pc:#x}')
    o += sz
