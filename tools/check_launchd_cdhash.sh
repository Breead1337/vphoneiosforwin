#!/bin/bash
# Mount hybrid vol=1 (System) ro, extract /sbin/launchd, so we can compute its cdhash.
set -e
IMG=/home/ard/vrwork/root2.hybrid.img
KO=/home/ard/kbuild/apfs/apfs.ko
OUT=/home/ard/vrwork/launchd_hybrid
grep -q '^apfs ' /proc/modules || insmod "$KO"
LOOP=$(losetup -f)
losetup -o 1048576 "$LOOP" "$IMG"
MNT=$(mktemp -d)
cleanup() { umount -q "$MNT" 2>/dev/null || true; losetup -d "$LOOP" 2>/dev/null || true; rmdir "$MNT" 2>/dev/null || true; }
trap cleanup EXIT
mount -t apfs -o ro,vol=1 "$LOOP" "$MNT"
ls -la "$MNT/sbin/launchd"
cp "$MNT/sbin/launchd" "$OUT"
chmod 0666 "$OUT"
echo "extracted -> $OUT ($(stat -c %s "$OUT") bytes)"
