#!/bin/bash
C=/home/ard/vrwork/boot_panic.console
k=0
while [ $k -lt 55 ]; do
  sleep 10; k=$((k+1))
  if grep -aqiE "panic|Original panic string|mounting volume Data" "$C" 2>/dev/null && grep -aq "mounting volume Data" "$C" 2>/dev/null; then
    if grep -aqiE "panic\(|Original panic|@.*apfs|assert|Corefile" "$C" 2>/dev/null; then echo "PANIC/crash ctx ~$((k*10))s"; sleep 5; break; fi
  fi
done
echo "=== panic/assert/apfs lines around crash ==="; grep -anaiE "panic|assert|Original panic|apfs|keybag|media|crypto|Corefile" "$C" 2>/dev/null | tail -30 | cut -c1-160
echo "=== markers ==="; grep -ac "mounting volume Data" "$C"; grep -ac "Corefile" "$C"
echo "=== console tail 12 ==="; grep -avE "^\[SVC" "$C" | tail -12 | cut -c1-150
