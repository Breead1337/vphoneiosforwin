#!/bin/bash
SL=/home/ard/vrwork/svc.log
echo "=== first line where child dyld (0x103xxxx) appears ==="
grep -anE 'pc=0x103[0-9a-f]{5}' "$SL" | head -3 | cut -c1-140
echo "=== ALL child (0x103xxxx) EL0 syscalls (its whole life) ==="
grep -aE 'pc=0x103[0-9a-f]{5}' "$SL" | cut -c1-150
echo "=== did child open the dyld cache dir/files? ==="
grep -aE 'pc=0x103[0-9a-f]{5}' "$SL" | grep -aoE 's[0-9]="[^"]*(dyld|Caches|cryptex)[^"]*"' | sort -u
echo "=== posix_spawn args (what launchd launched) ==="
grep -aE '\(posix_spawn\)' "$SL" | cut -c1-160 | tail -5
