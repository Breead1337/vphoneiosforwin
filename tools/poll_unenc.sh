#!/bin/bash
C=/home/ard/vrwork/boot_unenc.console; E=/home/ard/vrwork/exc.log
k=0
while [ $k -lt 45 ]; do
  sleep 8; k=$((k+1))
  if grep -aq 'Corefile is not yet' "$C" 2>/dev/null; then echo "crash ~$((k*8))s"; sleep 3; break; fi
  if grep -aq 'mount-complete volume Data' "$C" 2>/dev/null; then echo "DATA MOUNTED ~$((k*8))s"; sleep 6; break; fi
done
echo "=== Data mount result ==="; grep -aE 'mounting volume Data|mount-complete volume Data|failed' "$C" | grep -ai data | head
echo "=== volumes mounted ==="; grep -aoE 'mount-complete volume [A-Za-z]+' "$C" | sort -u
echo "=== boot tasks ==="; grep -aoE '\([a-z0-9-]+\) <Notice>: Doing boot task' "$C" | sort -u | wc -l
echo "=== crash/corefile ==="; grep -ac Corefile "$C"
echo "=== console tail 12 (past Data) ==="; awk '/mounting volume Data/{f=1} f' "$C" | grep -avE '^\[SVC' | head -16 | cut -c1-150
