import struct

f = r"D:\vphonewin\fw\cloud\raw\LLB.vresearch101.RELEASE.bin"
d = open(f, "rb").read()

tags = [
    ('ibot', 0x746f6269),
    ('dtre', 0x65727464),
    ('illb', 0x626c6c69),
    ('sptm', 0x6d747073),
    ('txm ', 0x206d7874),
    ('krnl', 0x6c6e726b),
    ('logo', 0x6f676f6c),
    ('recm', 0x6d636572),
    ('diag', 0x67616964),
    ('sepf', 0x66706573),
]

for name, val in tags:
    b_val = struct.pack('<I', val)
    cnt = d.count(b_val)
    positions = []
    idx = 0
    while True:
        pos = d.find(b_val, idx)
        if pos == -1: break
        positions.append(hex(pos))
        idx = pos + 1
    print(f"Tag '{name}' (0x{val:08x}): count={cnt}, offsets={positions[:5]}")
