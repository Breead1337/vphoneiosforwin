#!/bin/bash
SL=/home/ard/vrwork/svc.log
echo "=== shared_region_check_np (294=0x126) callers ==="
grep -aE 'x16=0x126 ' "$SL" | cut -c1-110 | head -6
echo "=== shared_region_map_and_slide_np (438=0x1b6) ==="
grep -aE 'x16=0x1b6 ' "$SL" | cut -c1-130 | head -6
echo "=== any 'map_with_linking' / shared_region variants (0x1b5..0x1b8) ==="
for h in 0x1b4 0x1b5 0x1b6 0x1b7 0x1b8; do
  c=$(grep -acE "x16=$h " "$SL"); echo "  syscall $h : $c calls"
done
echo "=== distinct UNIX syscall numbers used by CHILD (0x103xxxx) ==="
grep -aE 'pc=0x103[0-9a-f]{5}' "$SL" | grep -aoE 'x16=0x[0-9a-f]+' | sort | uniq -c
echo "=== distinct high-numbered syscalls overall (>0x1a0) ==="
grep -aoE 'x16=0x1[a-f][0-9a-f] ' "$SL" | sort | uniq -c | sort -rn | head -15
