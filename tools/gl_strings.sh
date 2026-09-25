#!/bin/bash
KC=/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin
killall -9 qemu-system-aarch64 2>/dev/null
echo "=== strings near gigalocker offsets in KC ==="
python3 - <<'PY'
f=open("/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin","rb").read()
import re
# find all ascii runs containing gigalocker or GL/class-key context
for m in re.finditer(rb'[ -~]{6,}', f):
    s=m.group()
    if b'gigalocker' in s.lower() or b'gigalock' in s.lower() or b'.gl' in s and b'xart' in s.lower():
        print(hex(m.start()), s.decode(errors='replace')[:120])
PY
