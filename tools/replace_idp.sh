#!/bin/bash
# Replace /usr/libexec/init_data_protection in root2.big.img System vol with patched binary.
set -e
IMG=/home/ard/vrwork/root2.big.img
NEW=/home/ard/vrwork/init_data_protection.patched
[ -f "$NEW" ] || { echo "no $NEW"; exit 1; }
grep -q '^apfs ' /proc/modules || insmod /home/ard/kbuild/apfs/apfs.ko
LOOP=$(losetup -f); losetup -o 1048576 "$LOOP" "$IMG"
MNT=$(mktemp -d)
trap 'umount -q "$MNT" 2>/dev/null||true; losetup -d "$LOOP" 2>/dev/null||true; rmdir "$MNT" 2>/dev/null||true' EXIT
# find the System volume (has /usr/libexec/init_data_protection)
for v in 1 0 2 3 4 5; do
  umount -q "$MNT" 2>/dev/null || true
  if mount -t apfs -o readwrite,vol=$v "$LOOP" "$MNT" 2>/dev/null; then
    if [ -f "$MNT/usr/libexec/init_data_protection" ]; then
      echo "found on vol=$v; old size $(stat -c %s "$MNT/usr/libexec/init_data_protection")"
      cp "$NEW" "$MNT/usr/libexec/init_data_protection"
      chmod 555 "$MNT/usr/libexec/init_data_protection"
      chown 0:0 "$MNT/usr/libexec/init_data_protection"
      sync
      echo "new size $(stat -c %s "$MNT/usr/libexec/init_data_protection")"
      exit 0
    fi
  fi
done
echo "init_data_protection not found in any volume"; exit 1
