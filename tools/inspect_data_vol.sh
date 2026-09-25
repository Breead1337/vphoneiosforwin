#!/bin/bash
IMG=/home/ard/vrwork/root2.big.img
grep -q '^apfs ' /proc/modules || insmod /home/ard/kbuild/apfs/apfs.ko
LOOP=$(losetup -f); losetup -o 1048576 "$LOOP" "$IMG"
MNT=$(mktemp -d)
trap 'umount -q "$MNT" 2>/dev/null||true; losetup -d "$LOOP" 2>/dev/null||true; rmdir "$MNT" 2>/dev/null||true' EXIT
for v in 0 1 2 3 4 5; do
  umount -q "$MNT" 2>/dev/null || true
  if mount -t apfs -o ro,vol=$v "$LOOP" "$MNT" 2>/dev/null; then
    # identify role by contents
    top=$(ls "$MNT" 2>/dev/null | tr "\n" " " | cut -c1-80)
    echo "vol=$v: $top"
  else
    echo "vol=$v: (mount failed)"
  fi
done
