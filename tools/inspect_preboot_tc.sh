#!/bin/bash
# Mount hybrid vol=0 (Preboot) ro, list FUD trust-cache img4s, copy StaticTrustCache out for inspection.
set -e
IMG=/home/ard/vrwork/root2.hybrid.img
KO=/home/ard/kbuild/apfs/apfs.ko
grep -q '^apfs ' /proc/modules || insmod "$KO"
LOOP=$(losetup -f)
losetup -o 1048576 "$LOOP" "$IMG"
MNT=$(mktemp -d)
cleanup(){ umount -q "$MNT" 2>/dev/null||true; losetup -d "$LOOP" 2>/dev/null||true; rmdir "$MNT" 2>/dev/null||true; }
trap cleanup EXIT
mount -t apfs -o ro,vol=0 "$LOOP" "$MNT"
NSIH=$(cat "$MNT/active" | tr -d '[:space:]')
FUD="$MNT/$NSIH/usr/standalone/firmware/FUD"
echo "=== FUD dir listing ==="
ls -la "$FUD" 2>/dev/null
echo "=== firmware dir (parent) ==="
ls -la "$MNT/$NSIH/usr/standalone/firmware/" 2>/dev/null | grep -iE "trust|StaticTrust|tc"
STC=$(find "$MNT/$NSIH/usr/standalone/firmware" -iname "*StaticTrustCache*" 2>/dev/null | head -1)
echo "StaticTrustCache path: $STC"
if [ -n "$STC" ]; then
  cp "$STC" /home/ard/vrwork/preboot_static_tc.img4
  chmod 0666 /home/ard/vrwork/preboot_static_tc.img4
  echo "copied -> /home/ard/vrwork/preboot_static_tc.img4 ($(stat -c %s "$STC") bytes)"
fi
