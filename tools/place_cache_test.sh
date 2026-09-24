#!/bin/bash
# De-risk test: place main dyld cache + first subcache at the cryptex path in the rootfs,
# to see if dyld finds it there (no real graft) and whether the 26.1 cache is version-accepted.
set -e
HYB=/home/ard/vrwork/root2.hybrid.img
CRY=/home/ard/vrwork/cryptex/043-54303-126.dmg
grep -q '^apfs ' /proc/modules || insmod /home/ard/kbuild/apfs/apfs.ko
LC=$(losetup --show -f "$CRY"); MC=$(mktemp -d)
LH=$(losetup --show -f -o 1048576 "$HYB"); MH=$(mktemp -d)
cleanup(){ umount -q "$MC" 2>/dev/null||true; umount -q "$MH" 2>/dev/null||true; losetup -d "$LC" 2>/dev/null||true; losetup -d "$LH" 2>/dev/null||true; rmdir "$MC" "$MH" 2>/dev/null||true; }
trap cleanup EXIT
mount -t apfs -o ro,vol=0 "$LC" "$MC"
mount -t apfs -o readwrite,vol=1 "$LH" "$MH"
SRC="$MC/System/Library/Caches/com.apple.dyld"
DST="$MH/private/preboot/Cryptexes/OS/System/Library/Caches/com.apple.dyld"
mkdir -p "$DST"
echo "copying main + .01 ..."
cp "$SRC/dyld_shared_cache_arm64e" "$DST/"
cp "$SRC/dyld_shared_cache_arm64e.01" "$DST/"
sync
echo "placed:"; ls -la "$DST" | head
echo "df:"; df -h "$MH" | tail -1
