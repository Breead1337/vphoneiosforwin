#!/bin/bash
C=/home/ard/vrwork/boot_unenc.console; E=/home/ard/vrwork/exc.log
echo "=== everything after last Hardware mount (non-SVC) ==="
awk '/mount-complete volume Hardware/{f=1} f' "$C" | grep -avE '^\[SVC' | head -30 | cut -c1-150
echo "=== new panic reason via far=0xe00 first-dump regs? ==="
grep -aA6 'far=0xe00 ' "$E" 2>/dev/null | head -8
echo "=== boot tasks list ==="; grep -aoE '\([a-z0-9-]+\) <Notice>: Doing boot task' "$C" | sort -u
