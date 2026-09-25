#!/bin/bash
C=/home/ard/vrwork/boot_ks.console
i=0
while [ $i -lt 300 ]; do
  if grep -aqE 'Corefile is not yet|panic' "$C" 2>/dev/null; then echo "CRASH ~$((i*8))s"; break; fi
  # also stop if we clearly stalled: ondemand never after long time is fine, keep waiting
  sleep 8; i=$((i+1))
done
sleep 3
echo "=== reached Data mount? ==="; grep -ac 'mounting volume Data' "$C"
echo "=== boot tasks ==="; grep -aoE '\([a-z0-9-]+\) <Notice>: Doing boot task' "$C" | sort -u | tail -12
echo "=== near-null EL1 detailed dump(s) ==="; grep -aA9 'vbar=' /home/ard/vrwork/exc.log 2>/dev/null | tail -30
echo "=== last 5 exc.log ==="; tail -5 /home/ard/vrwork/exc.log 2>/dev/null
killall -9 qemu-system-aarch64 2>/dev/null; echo "(freed)"
