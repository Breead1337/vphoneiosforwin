#!/bin/bash
C=/home/ard/vrwork/boot_clean.console; E=/home/ard/vrwork/exc.log
k=0
while [ $k -lt 55 ]; do
  sleep 10; k=$((k+1))
  if grep -aq "far=0xe00" "$E" 2>/dev/null; then echo "GOT far=0xe00 ~$((k*10))s"; break; fi
  if grep -aq "far=0x4000" "$E" 2>/dev/null; then echo "PPL early far=0x4000 ~$((k*10))s"; break; fi
done
echo "=== far=0xe00 detailed dump ==="; grep -aA10 "far=0xe00" "$E" 2>/dev/null | head -14
echo "=== far=0x4000 dump (if PPL) ==="; grep -aA10 "far=0x4000" "$E" 2>/dev/null | head -14
echo "=== markers ondemand/data/corefile ==="; grep -ac "entering ondemand" "$C"; grep -ac "mounting volume Data" "$C"; grep -ac "Corefile" "$C"
echo "=== tail ==="; tail -3 "$C" | cut -c1-100
