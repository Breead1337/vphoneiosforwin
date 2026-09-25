#!/bin/bash
C=/home/ard/vrwork/boot_exc3.console
i=0
while [ $i -lt 80 ]; do
  if grep -aqE 'Corefile is not yet|panic' "$C" 2>/dev/null; then echo "CRASH ~$((i*8))s"; break; fi
  sleep 8; i=$((i+1))
done
sleep 3
echo "=== boot tasks reached ==="; grep -aoE '\([a-z0-9-]+\) <Notice>: Doing boot task' "$C" | sort -u | tail
echo "=== reached Data mount? ==="; grep -ac 'mounting volume Data' "$C"
echo "=== ALL detailed near-null EL1 dumps (vbar + regs + insn) ==="
grep -aA9 'vbar=' /home/ard/vrwork/exc.log 2>/dev/null | tail -40
echo "=== last 6 exc.log lines ==="; tail -6 /home/ard/vrwork/exc.log
killall -9 qemu-system-aarch64 2>/dev/null; echo "(freed)"
