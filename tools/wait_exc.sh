#!/bin/bash
C=/home/ard/vrwork/boot_exc.console
i=0
while [ $i -lt 70 ]; do
  if grep -aqE 'Corefile is not yet|mount-complete volume Data|panic' "$C" 2>/dev/null; then echo "CRASH/DATA ~$((i*8))s"; break; fi
  sleep 8; i=$((i+1))
done
sleep 3
echo "=== data mount + crash console ==="; awk '/mount-phase-2/{f=1} f' "$C" | grep -avE '^\[SVC' | head -14
echo "=== exc.log tail (last aborts; fatal = last EL0 one) ==="
tail -25 /home/ard/vrwork/exc.log 2>/dev/null
killall -9 qemu-system-aarch64 2>/dev/null; echo "(freed)"
