#!/bin/bash
C=/home/ard/vrwork/boot_exc2.console
i=0
while [ $i -lt 70 ]; do
  if grep -aqE 'Corefile is not yet|panic' "$C" 2>/dev/null; then echo "CRASH ~$((i*8))s"; break; fi
  sleep 8; i=$((i+1))
done
sleep 3
echo "=== near-null EL1 abort detailed dump (first occurrence) ==="
grep -aA9 'far=0xe00' /home/ard/vrwork/exc.log 2>/dev/null | head -30
killall -9 qemu-system-aarch64 2>/dev/null; echo "(freed)"
