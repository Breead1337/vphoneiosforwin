#!/bin/bash
SL=/home/ard/vrwork/svc.log
C=/home/ard/vrwork/boot_dp.console
echo "=== last 20 EL0 syscalls (crash context) ==="
grep -aE '^\[SVC    ' "$SL" | tail -20 | cut -c1-125
echo "=== last 25 console lines (all) ==="
tail -25 "$C" | cut -c1-150
