#!/bin/bash
C=/home/ard/vrwork/boot_ln.console; E=/home/ard/vrwork/exc.log
k=0
while [ $k -lt 55 ]; do
  sleep 10; k=$((k+1))
  if grep -aq "far=0xe00" "$E" 2>/dev/null; then echo "GOT far=0xe00 ~$((k*10))s"; break; fi
  if grep -aq "Corefile is not yet" "$C" 2>/dev/null; then echo "crash ~$((k*10))s"; sleep 4; break; fi
done
echo "=== far=0xe00 DETAILED (vbar+regs+insn) ==="; grep -aA10 "far=0xe00" "$E" 2>/dev/null | head -14
echo "=== any near-null aborts ==="; grep -a "far=0x" "$E" 2>/dev/null | tail -6
echo "=== markers: ondemand/data/corefile ==="; grep -ac "entering ondemand" "$C"; grep -ac "mounting volume Data" "$C"; grep -ac "Corefile" "$C"
echo "=== tail ==="; tail -3 "$C" | cut -c1-100
