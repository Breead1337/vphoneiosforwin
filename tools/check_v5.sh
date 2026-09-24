#!/bin/bash
C=/home/ard/vrwork/boot_v5.console
SL=/home/ard/vrwork/svc.log
echo "=== process starts (distinct .01 cache opens = processes that mapped cache) ==="
grep -ac 'dyld_shared_cache_arm64e\.01"' "$SL"
echo "=== out of range bind (child crash) count ==="
grep -ac 'out of range bind' "$C"
echo "=== child (0x103xxxx) opened cache files? ==="
grep -aE 'pc=0x10[0-9a-f]{6}' "$SL" | grep -aoE 'dyld_shared_cache_arm64e(\.[0-9a-z]+)?' | sort -u | head
echo "=== distinct ASLR bases seen doing cache-open (463=x16 0x1cf) ==="
grep -aE 'x16=0x1cf ' "$SL" | grep -aoE 'pc=0x[0-9a-f]+' | sed -E 's/(0x..).*/\1/' | sort | uniq -c
echo "=== console: launchd / boot task / spawn / panic / SpringBoard ==="
grep -anE 'hello from launchd|boot task|Doing boot|out of range|Corefile|launchd|SpringBoard|backboard|posix_spawn|exec' "$C" | tail -25 | cut -c1-150
echo "=== executables spawned ==="
grep -aoE '"/(sbin|usr/sbin|usr/libexec|System/Library/CoreServices|bin|usr/bin)/[A-Za-z0-9_./-]+"' "$SL" | sort -u | head -40
echo "=== svc.log size ==="; wc -l "$SL"
