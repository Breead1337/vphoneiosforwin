# tbstat.py LOG [panic-pcs...] — parse qemu -d exec log: last TBs, hot TBs, exceptions
import re, sys, collections
L = open(sys.argv[1], errors='ignore').read().splitlines()
panic = {int(x, 16) for x in sys.argv[2:]}
pcs = []
for i, l in enumerate(L):
    m = re.search(r'Trace \d+: \S+ \[[0-9a-f]+/([0-9a-f]+)/', l)
    if m: pcs.append(int(m.group(1), 16))
print('TBs', len(pcs))
hit = [k for k, pc in enumerate(pcs) if any(0 <= pc - x < 0x40 for x in panic)]
k = hit[0] if hit else len(pcs) - 1
print('panic TB#', hit[0] if hit else None)
print('before:', ' '.join(hex(p) for p in pcs[max(0, k - 50):k + 1]))
print('hot last 200k:', [(hex(p), n) for p, n in collections.Counter(pcs[-200000:]).most_common(12)])
