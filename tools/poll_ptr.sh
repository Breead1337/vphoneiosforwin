#!/bin/bash
C=/home/ard/vrwork/boot_ptr.console; E=/home/ard/vrwork/exc.log
k=0
while [ $k -lt 45 ]; do
  sleep 8; k=$((k+1))
  if grep -aq 'Corefile is not yet' "$C" 2>/dev/null; then echo "crash ~$((k*8))s"; sleep 3; break; fi
done
echo "=== PTR-follow (panic reason candidates) ==="; grep -a 'PTR@' "$E" 2>/dev/null | head -20
echo "=== PSTR ==="; grep -a 'PSTR@' "$E" 2>/dev/null | grep -aivE 'iBoot|VRESEARCH|Compute|Darwin Kernel|Compatibility|E35C|[0-9A-F]{8}-[0-9A-F]{4}' | head -15
echo "=== far type + Data/Corefile ==="; grep -ac 'far=0x4000' "$E"; grep -ac 'far=0xe00 ' "$E"; grep -ac 'mounting volume Data' "$C"; grep -ac Corefile "$C"
