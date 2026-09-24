#!/bin/bash
SL=/home/ard/vrwork/svc.log
C=/home/ard/vrwork/boot_v5.console
echo "=== last subcache any process reached ==="
grep -aoE 'dyld_shared_cache_arm64e\.[0-9]+' "$SL" | sort -t. -k2 -n | tail -3
echo "=== last 20 EL0 svc lines (crash context) ==="
grep -aE '^\[SVC    ' "$SL" | tail -20 | cut -c1-135
echo "=== distinct pc-base prefixes of cache-opening (which processes) ==="
grep -aE 'x16=0x1cf ' "$SL" | grep -aoE 'pc=0x1[0-9a-f]{8}' | sed -E 's/(pc=0x1[0-9a-f]{2}).*/\1/' | sort | uniq -c
echo "=== console around 2nd boot ignition+crash (lines 380-410) ==="
sed -n '400,412p' "$C" | cut -c1-140
echo "=== was 'entering ondemand' present? ==="
grep -ac 'entering ondemand' "$C"
