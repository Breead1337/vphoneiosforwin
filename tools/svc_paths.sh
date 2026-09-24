#!/bin/bash
SL=/home/ard/vrwork/svc.log
echo "=== all distinct s0/s1/s2 strings that are NOT dyld_v1/dyld_shared_cache (file paths etc) ==="
grep -aoE 's[012]="[^"]+"' "$SL" | sed -E 's/^s[012]=//' | sort -u | grep -avE 'dyld_v1|dyld_shared_cache' | head -60
echo "=== EL0 (userspace, non-GL) syscalls in last 400 lines with names ==="
grep -aE '^\[SVC    ' "$SL" | tail -40 | cut -c1-160
echo "=== last 3 lines verbatim ==="
tail -3 "$SL" | cut -c1-200
