#!/bin/bash
# Build a bigger hybrid image = fresh 28G 2-vol APFS container, copy Preboot(vol0)+System(vol1)
# from the working root2.hybrid.img, then add the COMPLETE dyld shared cache (minus .symbols)
# at dyld's classic first search path /System/Library/Caches/com.apple.dyld/.
# qemu MUST be down. Run as root.
set -e
W=/home/ard/vrwork
OLD=$W/root2.hybrid.img
NEW=$W/root2.big.img
CRY=$W/cryptex/043-54303-126.dmg
MK=/home/ard/kbuild/apfsprogs/mkapfs/mkapfs
KO=/home/ard/kbuild/apfs/apfs.ko
SIZEG=${SIZEG:-28}

echo "qemu procs: $(ps -C qemu-system-aar --no-headers | wc -l)"
[ "$(ps -C qemu-system-aar --no-headers | wc -l)" = "0" ] || { echo "QEMU RUNNING - abort"; exit 1; }
grep -q '^apfs ' /proc/modules || insmod "$KO"

echo "=== [1/5] mkroot $SIZEG G ==="
MKAPFS=$MK APFS_KO=$KO bash /mnt/d/vphonewin/tools/mkroot.sh "$NEW" "$SIZEG"

# loop for NEW container (GPT part at 1MiB)
LN=$(losetup --show -f -o 1048576 "$NEW")
LO=$(losetup --show -f -o 1048576 "$OLD")
MO=$(mktemp -d); MN=$(mktemp -d)
cleanup(){ umount -q "$MO" 2>/dev/null||true; umount -q "$MN" 2>/dev/null||true; losetup -d "$LO" 2>/dev/null||true; losetup -d "$LN" 2>/dev/null||true; rmdir "$MO" "$MN" 2>/dev/null||true; }
trap cleanup EXIT

echo "=== [2/5] copy vol=0 Preboot (boot store + StaticTrustCache) ==="
mount -t apfs -o ro,vol=0 "$LO" "$MO"
mount -t apfs -o readwrite,vol=0 "$LN" "$MN"
cp -a "$MO"/. "$MN"/
sync; umount "$MO"; umount "$MN"

echo "=== [3/5] copy vol=1 System (iPhone-OS rootfs) ==="
mount -t apfs -o ro,vol=1 "$LO" "$MO"
mount -t apfs -o readwrite,vol=1 "$LN" "$MN"
time cp -a "$MO"/. "$MN"/
sync; umount "$MO"

echo "=== [4/5] add complete dyld cache at classic path ==="
LC=$(losetup --show -f "$CRY"); MC=$(mktemp -d)
mount -t apfs -o ro,vol=0 "$LC" "$MC"
SRC="$MC/System/Library/Caches/com.apple.dyld"
DST="$MN/System/Library/Caches/com.apple.dyld"
mkdir -p "$DST"
# copy every subcache EXCEPT the 999MB debug .symbols
for f in "$SRC"/dyld_shared_cache_arm64e*; do
  b=$(basename "$f"); case "$b" in *.symbols) echo "skip $b";; *) cp "$f" "$DST/";; esac
done
# stale de-risk copies at cryptex graft path -> replace with symlink to the classic dir (hedge)
GP="$MN/private/preboot/Cryptexes/OS/System/Library/Caches"
rm -rf "$GP/com.apple.dyld" 2>/dev/null || true
mkdir -p "$GP"
ln -s /System/Library/Caches/com.apple.dyld "$GP/com.apple.dyld"
sync
echo "placed $(ls "$DST" | wc -l) files, $(du -sh "$DST" | cut -f1)"
umount "$MC"; losetup -d "$LC"; rmdir "$MC"
umount "$MN"

echo "=== [5/5] apfsck (on container loop dev, before detach) ==="
apfsck "$LN" 2>&1 | tail -6 || echo "(apfsck reported issues - review above)"
echo "DONE -> $NEW (apparent $(ls -la $NEW | awk '{print $5}') B, on-disk $(du -h $NEW|cut -f1))"
