#!/bin/bash
# Re-sign the patched dyld, add its new cdhash to the trust cache (merged3 + StaticTrustCache),
# apply the re-signed dyld to the image, inject the new StaticTrustCache. qemu down. root.
set -e
W=/home/ard/vrwork
TCDIR=/mnt/d/vphonewin/_work/tc
IMG=$W/root2.big.img
killall -9 qemu-system-aarch64 2>/dev/null || true; sleep 1
losetup -D 2>/dev/null || true

echo "=== [1] re-sign patched dyld ==="
python3 /mnt/d/vphonewin/tools/resign_dyld.py "$W/dyld_hybrid" "$W/dyld_resigned"
NEWCD=$(cat "$W/dyld_resigned.cdhash")
echo "new dyld cdhash = $NEWCD"

echo "=== [2] build merged3 (merged2 + new dyld cdhash) ==="
cp "$TCDIR/merged2.trst.bin" "$TCDIR/merged3.trst.bin"
python3 /mnt/d/vphonewin/tools/tc_append.py "$TCDIR/merged3.trst.bin" "$NEWCD"

echo "=== [3] build + inject StaticTrustCache from merged3 ==="
python3 /mnt/d/vphonewin/tools/build_static_tc.py "$TCDIR/merged3.trst.bin" "$W/new_static_tc_resign.img4"
IMG="$IMG" NEW="$W/new_static_tc_resign.img4" bash /mnt/d/vphonewin/tools/inject_static_tc.sh

echo "=== [4] apply re-signed dyld to image (System vol) ==="
grep -q '^apfs ' /proc/modules || insmod /home/ard/kbuild/apfs/apfs.ko
L=$(losetup --show -f -o 1048576 "$IMG"); M=$(mktemp -d)
trap 'umount -q "$M" 2>/dev/null||true; losetup -d "$L" 2>/dev/null||true; rmdir "$M" 2>/dev/null||true' EXIT
mount -t apfs -o readwrite,vol=1 "$L" "$M"
rm -f "$M/usr/lib/dyld"; cp "$W/dyld_resigned" "$M/usr/lib/dyld"; chmod 0755 "$M/usr/lib/dyld"
sync
python3 -c "d=open('$M/usr/lib/dyld','rb').read(); print('0x7e1a8 =', d[0x7e1a8:0x7e1ac].hex(), '(expect 1f2003d5 NOP)')"
umount "$M"; losetup -d "$L"; rmdir "$M"; trap - EXIT
chown ard:ard "$IMG"
echo "DONE. Boot with TC=$TCDIR/merged3.trst.bin"
