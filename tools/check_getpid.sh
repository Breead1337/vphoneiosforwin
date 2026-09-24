#!/bin/bash
SL=/home/ard/vrwork/svc.log
echo "=== getpid (x16=0x14) calls in trace (trampoline hits) ==="
grep -anE 'x16=0x14 ' "$SL" | cut -c1-130
echo "=== count ==="; grep -acE 'x16=0x14 ' "$SL"
echo "=== distinct pc-bases that opened cache (.01) ==="
grep -aE 'dyld_shared_cache_arm64e\.01"' "$SL" | grep -aoE 'pc=0x[0-9a-f]+' | sed -E 's/(0x..).*/\1/' | sort | uniq -c
echo "=== last 12 EL0 lines (crash ctx) ==="
grep -aE '^\[SVC    ' "$SL" | tail -12 | cut -c1-130
