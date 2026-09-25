#!/bin/bash
C=/home/ard/vrwork/boot_dp.console
SL=/home/ard/vrwork/svc.log
echo "qemu alive: $(ps -C qemu-system-aar --no-headers | wc -l)"
echo "=== everything after Data volume mount attempt (non-SVC) ==="
awk '/mounting volume Data/{f=1} f' "$C" | grep -avE '^\[SVC' | head -40
echo "=== posix_spawn count / last spawns ==="; grep -acE '\(posix_spawn\)' "$SL"
grep -aE '\(posix_spawn\)' "$SL" | grep -aoE 's1="[^"]*"' | tail -8
echo "=== child crashes (PTWALK/out-of-range/Assertion) ==="; grep -acE 'VR_PTWALK|out of range bind|Assertion failed' "$SL"
