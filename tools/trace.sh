# build, run N seconds with exec trace; print last TBs before the first pvpanic / panic function
bash /mnt/d/vphonewin/tools/build_inferno.sh >/dev/null || exit 1
T=${T:-8} D=${D:-,int,exec,nochain} bash /mnt/d/vphonewin/tools/run1.sh > $HOME/vrwork/run.out 2>&1
head -3 $HOME/vrwork/run.out; echo "--- uart:"; head -c 3000 $HOME/vrwork/vr.uart
python3 /mnt/d/vphonewin/tools/tbstat.py $HOME/vrwork/vr.log ${STOP:-10550c 105524}; exit
import re
L=open('$HOME/vrwork/vr.log',errors='ignore').read().splitlines()
pcs=[]
for i,l in enumerate(L):
    m=re.search(r'Trace \d+: \S+ \[\S+/([0-9a-f]+)/',l)
    if m: pcs.append((i,int(m.group(1),16)))
print('TBs', len(pcs), 'lines', len(L))
# first entry into panic 0x10550c / 0x105524
hit=[k for k,(i,pc) in enumerate(pcs) if pc in (0x10550c,0x105524)]
k=hit[0] if hit else len(pcs)
print('panic at TB#',k if hit else None)
seen=[]
for i,pc in pcs[max(0,k-60):k+1]:
    seen.append(hex(pc))
print(' '.join(seen))
PY
