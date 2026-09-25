#!/bin/bash
SL=/home/ard/vrwork/svc.log
# init_data_protection spawned 3rd; find its pc-base from the write of "init_data_protection:" or the .gl open
echo "=== opens/stats of .gl or xarts (any process) ==="
grep -aE '(open|stat|openat|getattrlist|mkdir)' "$SL" | grep -aiE 'xart|\.gl|gigalock' | cut -c1-170 | head -20
echo "=== last 30 EL0 syscalls before end (crash ctx) ==="
grep -aE '^\[SVC    ' "$SL" | tail -30 | cut -c1-120
