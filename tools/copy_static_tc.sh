#!/bin/bash
set -e
IMG=/home/ard/vrwork/root2.hybrid.img
grep -q '^apfs ' /proc/modules || insmod /home/ard/kbuild/apfs/apfs.ko
LOOP=$(losetup -f); losetup -o 1048576 "$LOOP" "$IMG"
MNT=$(mktemp -d)
trap 'umount -q "$MNT" 2>/dev/null||true; losetup -d "$LOOP" 2>/dev/null||true; rmdir "$MNT" 2>/dev/null||true' EXIT
mount -t apfs -o ro,vol=0 "$LOOP" "$MNT"
NSIH=$(cat "$MNT/active" | tr -d '[:space:]')
SRC="$MNT/$NSIH/usr/standalone/firmware/FUD/StaticTrustCache.img4"
cp "$SRC" /home/ard/vrwork/preboot_static_tc.img4
chmod 0666 /home/ard/vrwork/preboot_static_tc.img4
echo "copied $(stat -c %s "$SRC") bytes -> /home/ard/vrwork/preboot_static_tc.img4"
