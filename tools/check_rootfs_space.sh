#!/bin/bash
IMG=/home/ard/vrwork/root2.hybrid.img
grep -q '^apfs ' /proc/modules || insmod /home/ard/kbuild/apfs/apfs.ko
L=$(losetup --show -f -o 1048576 "$IMG"); M=$(mktemp -d)
trap 'umount -q "$M" 2>/dev/null||true; losetup -d "$L" 2>/dev/null||true; rmdir "$M" 2>/dev/null||true' EXIT
mount -t apfs -o ro,vol=1 "$L" "$M"
echo "=== df of vol=1 ==="; df -h "$M" | tail -2
echo "=== /private/preboot/Cryptexes ==="; ls -la "$M"/private/preboot/Cryptexes/ 2>/dev/null || echo "(none)"
echo "=== /private/preboot/Cryptexes/OS ==="; ls -la "$M"/private/preboot/Cryptexes/OS/ 2>/dev/null || echo "(none/empty)"
echo "=== /System/Library/Caches/com.apple.dyld (symlink?) ==="; ls -la "$M"/System/Library/Caches/com.apple.dyld 2>/dev/null || echo "(none)"
echo "=== /System/Library/Caches (list) ==="; ls -la "$M"/System/Library/Caches/ 2>/dev/null | head
