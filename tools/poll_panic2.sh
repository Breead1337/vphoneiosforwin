#!/bin/bash
C=/home/ard/vrwork/boot_panic.console
k=0
while [ $k -lt 55 ]; do
  sleep 10; k=$((k+1))
  if grep -aq "Corefile is not yet" "$C" 2>/dev/null; then echo "crash ~$((k*10))s"; sleep 4; break; fi
  if grep -aq "mounting volume Data" "$C" 2>/dev/null; then echo "data ~$((k*10))s"; fi
done
echo "=== NEW panic/assert lines (after Data mount) ==="
awk '/mount-phase-2|mounting volume Data/{f=1} f' "$C" | grep -aiE "panic|assert|Original panic|keybag|media|crypto|require|fault|abort|Corefile|SPTM" | head -25 | cut -c1-160
echo "=== console tail 14 ==="; grep -avE "^\[SVC" "$C" | tail -14 | cut -c1-155
echo "=== data/corefile ==="; grep -ac "mounting volume Data" "$C"; grep -ac "Corefile" "$C"
