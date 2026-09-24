#!/bin/bash
SL=/home/ard/vrwork/svc.log
echo "=== last 25 EL0 svc lines (crash context) ==="
grep -aE '^\[SVC    ' "$SL" | tail -25 | cut -c1-140
echo "=== distinct exec/open of boot-task binaries ==="
grep -aoE 's[0-9]="/[A-Za-z0-9_./-]+"' "$SL" | sort -u | grep -aviE 'dyld' | tail -40
echo "=== process starts count (.01) ==="; grep -ac 'dyld_shared_cache_arm64e\.01"' "$SL"
