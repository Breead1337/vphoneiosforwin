#!/bin/bash
C=/home/ard/vrwork/boot_panic.console
k=0
while [ $k -lt 56 ]; do
  sleep 10; k=$((k+1))
  if grep -aq 'Corefile is not yet' "$C" 2>/dev/null; then echo "corefile ~$((k*10))s"; sleep 3; break; fi
  if grep -aq 'Original panic string' "$C" 2>/dev/null; then echo "PANIC STRING ~$((k*10))s"; sleep 3; break; fi
  if ! ps -C qemu-system-aar --no-headers >/dev/null 2>&1; then echo "qemu exited ~$((k*10))s"; break; fi
done
echo "=== Data / Corefile ==="; grep -ac 'mounting volume Data' "$C"; grep -ac 'Corefile' "$C"
echo "=== panic/original-panic lines ==="; grep -anaiE 'Original panic|panic\(|require|kernel data abort|SPTM|nonzero|assert' "$C" | tail -20 | cut -c1-170
echo "=== after Data mount ==="; awk '/mounting volume Data/{f=1} f' "$C" | grep -avE '^\[SVC' | head -18 | cut -c1-160
