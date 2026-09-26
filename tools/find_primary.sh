#!/bin/bash
E=/home/ard/vrwork/exc.log
echo "=== all EXC lines, pc histogram (find non-copyio primary) ==="
grep -aE '^\[EXC' "$E" | grep -aoE 'pc=0x[0-9a-f]+' | sort | uniq -c | sort -rn
echo "=== first 25 EXC lines in order ==="
grep -aE '^\[EXC' "$E" | head -25
