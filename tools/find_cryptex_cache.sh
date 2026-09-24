#!/bin/bash
DMG=/home/ard/vrwork/cryptex/043-54303-126.dmg
grep -q '^apfs ' /proc/modules || insmod /home/ard/kbuild/apfs/apfs.ko
L=$(losetup --show -f "$DMG"); M=$(mktemp -d)
trap 'umount -q "$M" 2>/dev/null||true; losetup -d "$L" 2>/dev/null||true; rmdir "$M" 2>/dev/null||true' EXIT
mount -t apfs -o ro,vol=0 "$L" "$M"
echo "=== cryptex top ==="; ls -la "$M" | head
echo "=== dyld_shared_cache files ==="; find "$M" -iname "dyld_shared_cache*" 2>/dev/null -exec ls -la {} \; | head -30
echo "=== System/Library/dyld ==="; ls -la "$M"/System/Library/dyld/ 2>/dev/null | head
echo "=== System/Library/Caches/com.apple.dyld ==="; ls -la "$M"/System/Library/Caches/com.apple.dyld/ 2>/dev/null | head -30
echo "=== is /usr/lib/libSystem.B.dylib here? ==="; ls -la "$M"/usr/lib/libSystem.B.dylib 2>/dev/null || echo "(no)"
