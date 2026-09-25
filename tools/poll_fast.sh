#!/bin/bash
C=/home/ard/vrwork/boot_fast.console; T0=$(cat /home/ard/vrwork/t0 2>/dev/null || echo 0)
el(){ echo $(( $(date +%s) - T0 ))s; }
k=0
while [ $k -lt 55 ]; do
  sleep 10; k=$((k+1))
  if grep -aq 'entering ondemand' "$C" 2>/dev/null && [ -z "$OND" ]; then OND=1; echo "ONDEMAND at $(el)"; fi
  if grep -aq 'mounting volume Data' "$C" 2>/dev/null; then echo "DATA MOUNT at $(el)"; fi
  if grep -aq 'Corefile is not yet' "$C" 2>/dev/null; then echo "crash at $(el)"; sleep 3; break; fi
  if grep -aq 'Original panic string' "$C" 2>/dev/null; then echo "PANIC STRING at $(el)"; sleep 3; break; fi
done
echo "=== ignition/ondemand/data/corefile ==="; grep -ac 'ignition sequence complete' "$C"; grep -ac 'entering ondemand' "$C"; grep -ac 'mounting volume Data' "$C"; grep -ac Corefile "$C"
echo "=== panic lines ==="; grep -anaiE 'Original panic|panic\(|require|kernel data abort|SPTM|assert' "$C" | tail -15 | cut -c1-170
echo "=== after Data mount ==="; awk '/mounting volume Data/{f=1} f' "$C" | grep -avE '^\[SVC' | head -18 | cut -c1-155
