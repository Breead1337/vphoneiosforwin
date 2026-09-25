#!/bin/bash
C=/home/ard/vrwork/${1:-boot_nohooks.console}
SL=/home/ard/vrwork/svc.log
i=0
while [ $i -lt 68 ]; do
  # stop when we see a definitive end state
  if grep -aqE "out of range bind|Assertion failed|VR_PTWALK end|SIGKILL of init|unexpected SIGKILL|cannot continue|Doing boot task" "$C" 2>/dev/null; then
     echo "MILESTONE hit ~$((i*8))s"; break; fi
  sleep 8; i=$((i+1))
done
echo "=== ignition/ondemand/hello/boot-task/crash markers ==="
grep -acE "ignition sequence complete" "$C" | sed "s/^/ignition_complete: /"
grep -acE "entering ondemand" "$C" | sed "s/^/ondemand: /"
grep -acE "Doing boot task" "$C" | sed "s/^/boot_task: /"
grep -aE "out of range bind|Assertion failed|SIGKILL|panic|cannot continue" "$C" | tail -4
echo "=== console tail 6 ==="; tail -6 "$C"
