#!/bin/bash
C=/home/ard/vrwork/boot_dp.console
SL=/home/ard/vrwork/svc.log
echo "qemu alive: $(ps -C qemu-system-aar --no-headers | wc -l)"
echo "Corefile crashes in console: $(grep -ac 'Corefile is not yet' "$C")"
echo "=== console lines AFTER last Data-mount line (progress after crash?) ==="
tail -8 "$C" | cut -c1-140
echo "=== FULL last svc line with all fields (crashing insn) ==="
grep -aE '^\[SVC    ' "$SL" | tail -1
echo "=== how many distinct pc-bases active in last 300 svc lines ==="
grep -aE '^\[SVC    ' "$SL" | tail -300 | grep -aoE 'pc=0x[0-9a-f]{3}' | sort | uniq -c
