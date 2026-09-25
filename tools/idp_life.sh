#!/bin/bash
SL=/home/ard/vrwork/svc.log
# find the pc-base of the process that wrote "gigalocker"/"Gigalocker" (init_data_protection)
echo "=== writes mentioning gigalocker/xart (identify pc-base) ==="
grep -aE 'Gigalocker|gigalocker|init_data_protection' "$SL" | grep -aoE 'pc=0x[0-9a-f]+' | sed -E 's/(pc=0x1[0-9a-f]{2}).*/\1/' | sort | uniq -c
echo "=== IOKit/service opens + xart file ops by init_data_protection (last spawn region) ==="
# the 3rd process: get lines after the 3rd posix_spawn
awk '/\(posix_spawn\)/{n++} n>=3' "$SL" | grep -aiE 'open|stat|IOServiceOpen|io_service|AppleSEP|sep|xart|\.gl|gigaloc|creat|mkdir|error|mach_msg' | cut -c1-160 | head -40
