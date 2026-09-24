#!/bin/bash
# Patch dyld at 0x7d98c (graft-stage tbz -> NOP: all cryptex graft failures become
# optional/non-fatal), re-sign, add new cdhash to TC (merged4), inject StaticTrustCache,
# apply to image. Starts from clean dyld_hybrid. qemu down. root.
set -e
W=/home/ard/vrwork
TCDIR=/mnt/d/vphonewin/_work/tc
IMG=$W/root2.big.img
killall -9 qemu-system-aarch64 2>/dev/null || true; sleep 1
losetup -D 2>/dev/null || true

echo "=== [1] patch 0x7d98c NOP + re-sign ==="
python3 /mnt/d/vphonewin/tools/resign_dyld.py "$W/dyld_hybrid" "$W/dyld_v4" "0x7d98c:1f2003d5"
NEWCD=$(cat "$W/dyld_v4.cdhash")

echo "=== [2] merged4 = merged2 + new cdhash ==="
cp "$TCDIR/merged2.trst.bin" "$TCDIR/merged4.trst.bin"
python3 /mnt/d/vphonewin/tools/tc_append.py "$TCDIR/merged4.trst.bin" "$NEWCD"

echo "=== [3] StaticTrustCache from merged4 + inject ==="
python3 /mnt/d/vphonewin/tools/build_static_tc.py "$TCDIR/merged4.trst.bin" "$W/static_tc_v4.img4"
IMG="$IMG" NEW="$W/static_tc_v4.img4" bash /mnt/d/vphonewin/tools/inject_static_tc.sh

echo "=== [4] apply dyld_v4 to image ==="
grep -q '^apfs ' /proc/modules || insmod /home/ard/kbuild/apfs/apfs.ko
L=$(losetup --show -f -o 1048576 "$IMG"); M=$(mktemp -d)
trap 'umount -q "$M" 2>/dev/null||true; losetup -d "$L" 2>/dev/null||true; rmdir "$M" 2>/dev/null||true' EXIT
mount -t apfs -o readwrite,vol=1 "$L" "$M"
rm -f "$M/usr/lib/dyld"; cp "$W/dyld_v4" "$M/usr/lib/dyld"; chmod 0755 "$M/usr/lib/dyld"
sync
python3 -c "d=open('$M/usr/lib/dyld','rb').read(); print('0x7d98c =', d[0x7d98c:0x7d990].hex(), '(NOP=1f2003d5)'); print('0x7e1a8 =', d[0x7e1a8:0x7e1ac].hex(), '(orig=97e2ff35)')"
umount "$M"; losetup -d "$L"; rmdir "$M"; trap - EXIT
chown ard:ard "$IMG"
echo "DONE. Boot TC=$TCDIR/merged4.trst.bin"
