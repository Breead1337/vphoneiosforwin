#!/bin/bash
set -e
IMG=/home/ard/vrwork/root2.hybrid.img
grep -q '^apfs ' /proc/modules || insmod /home/ard/kbuild/apfs/apfs.ko
LOOP=$(losetup -f); losetup -o 1048576 "$LOOP" "$IMG"
MNT=$(mktemp -d)
trap 'umount -q "$MNT" 2>/dev/null||true; losetup -d "$LOOP" 2>/dev/null||true; rmdir "$MNT" 2>/dev/null||true' EXIT
mount -t apfs -o ro,vol=1 "$LOOP" "$MNT"
echo "=== /System/Library/dyld ==="; ls -la "$MNT/System/Library/dyld/" 2>/dev/null || echo "(none)"
echo "=== any dyld_shared_cache in rootfs ==="; find "$MNT/System" -iname "dyld_shared_cache*" 2>/dev/null | head
echo "=== /System/Cryptexes ==="; ls -la "$MNT/System/Cryptexes/" 2>/dev/null || echo "(none)"
echo "=== /System/Volumes/Preboot/Cryptexes ==="; ls -la "$MNT/System/Volumes/Preboot/Cryptexes/" 2>/dev/null || echo "(none)"
echo "=== /usr/lib/libSystem.B.dylib exists? ==="; ls -la "$MNT/usr/lib/libSystem.B.dylib" 2>/dev/null || echo "(no standalone libSystem - it is in the shared cache)"
echo "=== /usr/lib/dyld ==="; ls -la "$MNT/usr/lib/dyld" 2>/dev/null || echo "(none)"
