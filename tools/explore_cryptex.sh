#!/bin/bash
set -e
DMG=/home/ard/vrwork/cryptex/043-54303-126.dmg
grep -q '^apfs ' /proc/modules || insmod /home/ard/kbuild/apfs/apfs.ko
LOOP=$(losetup -f); losetup -o 1048576 "$LOOP" "$DMG"
MNT=$(mktemp -d)
trap 'umount -q "$MNT" 2>/dev/null||true; losetup -d "$LOOP" 2>/dev/null||true; rmdir "$MNT" 2>/dev/null||true' EXIT
# try vol 0..2
for V in 0 1 2; do
  if mount -t apfs -o ro,vol=$V "$LOOP" "$MNT" 2>/dev/null; then
    echo "=== mounted vol=$V ==="
    ls "$MNT" | head
    echo "--- find dyld_shared_cache ---"
    find "$MNT" -iname "dyld_shared_cache*" 2>/dev/null | head -20
    echo "--- System/Library/dyld ---"
    ls -la "$MNT"/System/Library/dyld/ 2>/dev/null | head
    echo "--- System/Library/Caches/com.apple.dyld ---"
    ls -la "$MNT"/System/Library/Caches/com.apple.dyld/ 2>/dev/null | head
    umount -q "$MNT" || true
    break
  fi
done
