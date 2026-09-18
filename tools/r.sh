DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
T=4 STOP=0 bash "$DIR/trace.sh" >/dev/null 2>&1
python3 - <<PY
import re
L=open("/root/vrwork/vr.log",errors="ignore").read().splitlines() if False else open(__import__("os").path.expanduser("~/vrwork/vr.log"),errors="ignore").read().splitlines()
pcs=[int(m.group(1),16) for l in L for m in [re.search(r"Trace \d+: 0x[0-9a-f]+ \[[0-9a-f]+/0*([0-9a-f]+)/",l)] if m]
tail=pcs[-4000:]
from collections import Counter
print("top:",[(hex(p),n) for p,n in Counter(tail).most_common(10)])
# find shortest period at end
s=tail
for T in range(1,200):
    if len(s)>2*T and s[-T:]==s[-2*T:-T]:
        cyc=s[-T:]
        print("period",T,"cycle:",[hex(x) for x in cyc[:40]]); break
PY
