#!/bin/bash
# Build merged2 TC (merged + dyld-cache cdhashes) + StaticTrustCache.img4, inject into big image.
# qemu must be down. Run as root.
set -e
W=/home/ard/vrwork
CRY=$W/cryptex/043-54303-126.dmg
TCDIR=/mnt/d/vphonewin/_work/tc
MERGED=$TCDIR/merged.trst.bin
MERGED2=$TCDIR/merged2.trst.bin
IMG4=$W/new_static_tc_dsc.img4
BIG=$W/root2.big.img

killall -9 qemu-system-aarch64 2>/dev/null || true; sleep 1
grep -q '^apfs ' /proc/modules || insmod /home/ard/kbuild/apfs/apfs.ko

L=$(losetup --show -f "$CRY"); M=$(mktemp -d)
trap 'umount -q "$M" 2>/dev/null||true; losetup -d "$L" 2>/dev/null||true; rmdir "$M" 2>/dev/null||true' EXIT
mount -t apfs -o ro,vol=0 "$L" "$M"
python3 /mnt/d/vphonewin/tools/build_dsc_tc.py "$M/System/Library/Caches/com.apple.dyld" "$MERGED" "$MERGED2" "$IMG4"
umount "$M"; losetup -d "$L"; rmdir "$M"; trap - EXIT

echo "=== inject StaticTrustCache into $BIG ==="
IMG="$BIG" NEW="$IMG4" bash /mnt/d/vphonewin/tools/inject_static_tc.sh
echo DONE
