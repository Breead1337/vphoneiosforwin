#!/bin/bash
C=/home/ard/vrwork/boot_el1.console; E=/home/ard/vrwork/exc.log
k=0
while [ $k -lt 40 ]; do
  sleep 8; k=$((k+1))
  if grep -aq 'Corefile is not yet' "$C" 2>/dev/null; then echo "crash ~$((k*8))s"; sleep 3; break; fi
done
echo "=== ALL EL1 aborts in sequence (primary fault first, then panic-handler) ==="
grep -aE '^\[EXC' "$E" 2>/dev/null | head -30
echo "=== data/corefile ==="; grep -ac 'mounting volume Data' "$C"; grep -ac Corefile "$C"
