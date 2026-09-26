#!/bin/bash
E=/home/ard/vrwork/exc.log
echo "total lines: $(wc -l < "$E")"
echo "=== first 12 EXC lines ==="
grep -aE '^\[EXC' "$E" | head -12
echo "=== far-value histogram ==="
grep -aoE 'far=0x[0-9a-f]+' "$E" | sort | uniq -c | sort -rn | head
echo "=== distinct crash pc (EL1) ==="
grep -aE '^\[EXC.*EL1' "$E" | grep -aoE 'pc=0x[0-9a-f]+' | sort | uniq -c | sort -rn | head
