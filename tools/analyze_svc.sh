#!/bin/bash
SL=/home/ard/vrwork/svc.log
echo "=== size ==="; ls -la "$SL"; wc -l "$SL"
echo "=== last 8 distinct subcache names touched ==="
grep -aoE 'dyld_shared_cache_arm64e(\.[0-9a-z]+)?' "$SL" | uniq | tail -8
echo "=== last 30 lines (trunc 220) ==="
tail -30 "$SL" | cut -c1-220
echo "=== count of each syscall name in LAST 200 lines (detect spin) ==="
tail -200 "$SL" | grep -aoE '\([a-z_/]+\)' | sort | uniq -c | sort -rn | head -15
