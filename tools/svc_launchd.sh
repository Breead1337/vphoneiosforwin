#!/bin/bash
SL=/home/ard/vrwork/svc.log
echo "=== size/lines ==="; ls -la "$SL"; wc -l "$SL"
echo "=== last subcache touched ==="; grep -aoE 'dyld_shared_cache_arm64e(\.[0-9a-z]+)?' "$SL" | tail -1
echo "=== FIRST openat/open with a real path AFTER dyld (launchd config?) ==="
grep -anE 'openat|"/[A-Za-z]' "$SL" | grep -avE 'dyld_v1|dyld_shared_cache' | head -30 | cut -c1-200
echo "=== line number where last subcache appears vs total ==="
grep -an 'dyld_shared_cache_arm64e.79' "$SL" | tail -1
echo "=== LAST 25 lines (trunc 200) ==="
tail -25 "$SL" | cut -c1-200
echo "=== distinct EL0 syscall x16 in last 500 lines (spin fingerprint) ==="
grep -aE '^\[SVC    ' "$SL" | tail -500 | grep -aoE 'x16=0x[0-9a-f]+' | sort | uniq -c | sort -rn | head
