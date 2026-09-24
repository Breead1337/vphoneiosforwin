#!/bin/bash
# Mount cryptex ro and compute cdhashes of the dyld cache files vs merged TC. qemu must be down.
set -e
killall -9 qemu-system-aarch64 2>/dev/null || true; sleep 1
CRY=/home/ard/vrwork/cryptex/043-54303-126.dmg
grep -q '^apfs ' /proc/modules || insmod /home/ard/kbuild/apfs/apfs.ko
L=$(losetup --show -f "$CRY"); M=$(mktemp -d)
trap 'umount -q "$M" 2>/dev/null||true; losetup -d "$L" 2>/dev/null||true; rmdir "$M" 2>/dev/null||true' EXIT
mount -t apfs -o ro,vol=0 "$L" "$M"
python3 /mnt/d/vphonewin/tools/dsc_cdhashes.py "$M/System/Library/Caches/com.apple.dyld" /mnt/d/vphonewin/_work/tc/merged.trst.bin
