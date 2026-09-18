# xref.py FILE (STRING|0xVA) — find adrp+add/ldr references to a string (or VA) in a Mach-O's exec segments
import sys, struct
f, what = sys.argv[1], sys.argv[2]
d = open(f, 'rb').read()
segs = []
ncmds = struct.unpack('<I', d[16:20])[0]; o = 32
for _ in range(ncmds):
    cmd, sz = struct.unpack('<II', d[o:o+8])
    if cmd == 0x19:
        vm, vs, fo, fs, mp, ip = struct.unpack('<QQQQII', d[o+24:o+64]); segs.append((vm, fs, fo, ip))
    o += sz
def f2v(off): return next(vm + off - fo for vm, fs, fo, ip in segs if fo <= off < fo + fs)
if what.startswith('0x'):
    targets = [int(what, 16)]
else:
    targets, i = [], d.find(what.encode())
    while i >= 0:
        s = d.rfind(b'\0', 0, i) + 1; targets.append(f2v(s)); print(f'string @ {f2v(s):#x}: {d[s:d.find(b"\0", i)][:120]}')
        i = d.find(what.encode(), i + 1)
for vm, fs, fo, ip in segs:
    if not ip & 4: continue
    for i in range(0, fs - 8, 4):
        w = struct.unpack('<I', d[fo+i:fo+i+4])[0]
        if (w & 0x9f000000) != 0x90000000: continue
        pc = vm + i; imm = ((w >> 29) & 3) | (((w >> 5) & 0x7ffff) << 2)
        if imm >> 20: imm -= 1 << 21
        page = (pc & ~0xfff) + (imm << 12); rd = w & 31
        for j in range(1, 6):
            w2 = struct.unpack('<I', d[fo+i+4*j:fo+i+4*j+4])[0]
            if (w2 & 0xffc00000) == 0x91000000 and (w2 >> 5) & 31 == rd:
                if page + ((w2 >> 10) & 0xfff) in targets: print(f'ref {pc:#x}')
                break
