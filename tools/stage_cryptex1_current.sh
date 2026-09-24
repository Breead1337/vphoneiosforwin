#!/bin/bash
set -e
IMG=/home/ard/vrwork/root2.big.img
killall -9 qemu-system-aarch64 2>/dev/null || true; sleep 1
losetup -D 2>/dev/null || true   # detach stale loops
grep -q '^apfs ' /proc/modules || insmod /home/ard/kbuild/apfs/apfs.ko
L=$(losetup --show -f -o 1048576 "$IMG"); M=$(mktemp -d)
trap 'umount -q "$M" 2>/dev/null||true; losetup -d "$L" 2>/dev/null||true; rmdir "$M" 2>/dev/null||true' EXIT
mount -t apfs -o readwrite,vol=0 "$L" "$M"
mkdir -p "$M/cryptex1/current"
sync
echo "vol0 cryptex1 tree:"; ls -laR "$M/cryptex1"
umount "$M"; losetup -d "$L"; rmdir "$M"; trap - EXIT
chown ard:ard "$IMG"
echo DONE
