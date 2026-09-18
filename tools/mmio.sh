# run with MMIO tracing; summarize accesses per region/offset (first occurrences in order)
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
T=${T:-6} D=${D:-} EXTRA="--trace memory_region_ops_read --trace memory_region_ops_write $EXTRA" bash "$DIR/run1.sh" > ~/vrwork/run.out 2>&1
head -2 ~/vrwork/run.out; echo "--- uart:"; head -c 2000 ~/vrwork/vr.uart; echo
python3 - <<'PY'
import re, collections, os
L = open(os.path.expanduser('~/vrwork/vr.log'), errors='ignore').read().splitlines()
seq = []; cnt = collections.Counter()
for l in L:
    m = re.search(r'memory_region_ops_(read|write) cpu \d+ mr 0x[0-9a-f]+ addr (0x[0-9a-f]+) value (0x[0-9a-f]+) size (\d+) name \'([^\']*)\'', l)
    if not m: continue
    rw, addr, val, sz, name = m.groups()
    k = (name, rw, addr)
    if k not in cnt: seq.append((name, rw, addr, val))
    cnt[k] += 1
print('distinct', len(seq))
for name, rw, addr, val in seq[:int(os.environ.get('N', '200'))]:
    print(f'{name:28s} {rw:5s} {addr:>10s} {val:>12s} x{cnt[(name,rw,addr)]}')
other = [l for l in L if 'memory_region_ops' not in l]
print('--- other log:'); print('\n'.join(collections.Counter(other).keys().__iter__().__class__(other[:30]) if False else other[:30]))
PY
