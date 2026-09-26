#!/bin/bash
python3 - <<'PY'
KC="/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin"
f=open(KC,"rb").read(); BASE=0xfffffe0007004000
for va in [0xfffffe0007055498,0xfffffe00070552c8]:
    o=va-BASE; s=f[o:o+140].split(b"\0")[0]
    print(hex(va),":",repr(s))
PY
echo "=== APFS abort (0x3569f7a8) full line ==="
grep -aF 'pc=0xfffffe003569f7a8' /home/ard/vrwork/exc.log
echo "=== 0x92be7b0 abort full line ==="
grep -aF 'pc=0xfffffe00360a67b0' /home/ard/vrwork/exc.log
