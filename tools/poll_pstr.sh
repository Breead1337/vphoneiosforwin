#!/bin/bash
C=/home/ard/vrwork/boot_pstr.console; E=/home/ard/vrwork/exc.log
k=0
while [ $k -lt 45 ]; do
  sleep 8; k=$((k+1))
  if grep -aq 'Corefile is not yet' "$C" 2>/dev/null; then echo "crash ~$((k*8))s"; sleep 3; break; fi
done
echo "=== PSTR (panic reason strings from global) ==="; grep -a 'PSTR@' "$E" 2>/dev/null | head -40
echo "=== far=0xe00 dump head ==="; grep -aA3 'far=0xe00' "$E" 2>/dev/null | head -5
echo "=== data/corefile ==="; grep -ac 'mounting volume Data' "$C"; grep -ac Corefile "$C"
