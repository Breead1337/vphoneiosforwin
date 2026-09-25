#!/bin/bash
C=/home/ard/vrwork/boot_dp.console
i=0
while [ $i -lt 68 ]; do
  # stop on a clear post-data-protection signal or a crash
  if grep -aqE 'mount-complete volume Data|keybag|backboard|SpringBoard|logd|UserEventAgent|Failed to initialize gigalocker|panic|Corefile' "$C" 2>/dev/null; then
     echo "SIGNAL ~$((i*8))s"; break; fi
  sleep 8; i=$((i+1))
done
echo "=== boot tasks ==="; grep -aoE '\([a-z0-9-]+\) <Notice>: Doing boot task' "$C" | sort -u
echo "=== gigalocker outcome ==="; grep -aE 'gigalocker|Gigalocker' "$C" | tail -3
echo "=== mounts ==="; grep -aoE 'mount-complete volume [A-Za-z]+' "$C" | sort -u
echo "=== crash/panic ==="; grep -acE 'Corefile|out of range|Assertion|panic'  "$C"
echo "=== tail 14 ==="; tail -14 "$C"
