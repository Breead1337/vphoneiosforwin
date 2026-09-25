#!/bin/bash
SL=/home/ard/vrwork/svc.log
C=/home/ard/vrwork/boot_sweep.console
i=0
while [ $i -lt 200 ]; do
  if grep -aq "VR_PTWALK end" "$SL" 2>/dev/null; then echo "PTWALK READY ~$((i*8))s"; break; fi
  sleep 8; i=$((i+1))
done
echo "=== crash line ==="; grep -aE "out of range bind|Assertion failed" "$C" | head -2
echo "=== PTWALK ==="; awk '/VR_PTWALK \(child/{f=1} f{print} /VR_PTWALK end/{exit}' "$SL"
killall -9 qemu-system-aarch64 2>/dev/null; echo "(qemu freed)"
