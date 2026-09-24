#!/bin/bash
# Replace FUD/StaticTrustCache.img4 in hybrid Preboot with a merged trust cache (iPhone-OS cdhashes),
# so TXM (which loads THIS at secure boot, not the DT one) accepts iPhone-OS binaries.
set -e
IMG=${IMG:-/home/ard/vrwork/root2.hybrid.img}
NEW=${NEW:-/home/ard/vrwork/new_static_tc.img4}
[ -f "$NEW" ] || { echo "no $NEW"; exit 1; }
grep -q '^apfs ' /proc/modules || insmod /home/ard/kbuild/apfs/apfs.ko
LOOP=$(losetup -f); losetup -o 1048576 "$LOOP" "$IMG"
MNT=$(mktemp -d)
trap 'umount -q "$MNT" 2>/dev/null||true; losetup -d "$LOOP" 2>/dev/null||true; rmdir "$MNT" 2>/dev/null||true' EXIT
mount -t apfs -o readwrite,vol=0 "$LOOP" "$MNT"
NSIH=$(cat "$MNT/active" | tr -d '[:space:]')
DST="$MNT/$NSIH/usr/standalone/firmware/FUD/StaticTrustCache.img4"
[ -f "$DST" ] || { echo "no $DST"; exit 1; }
echo "old StaticTrustCache: $(stat -c %s "$DST") bytes"
cp "$NEW" "$DST"
sync
echo "new StaticTrustCache: $(stat -c %s "$DST") bytes (NSIH=$NSIH)"
