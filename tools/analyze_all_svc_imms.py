import re
from collections import Counter

c = Counter()
with open('/home/ard/vrwork/us.log', 'r', errors='ignore') as f:
    for line in f:
        m = re.search(r'with ESR 0x15/0x([0-9a-fA-F]+)', line)
        if m:
            esr = int(m.group(1), 16)
            imm = esr & 0xffff
            c[imm] += 1

print(f"Total unique SVC immediates: {len(c)}")
for imm, count in c.most_common(50):
    # check if signed 16-bit
    simm = imm if imm < 0x8000 else imm - 0x10000
    print(f"  imm=0x{imm:04x} ({imm:5d} / signed {simm:5d}): count={count}")
