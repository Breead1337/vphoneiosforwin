#!/bin/bash
# Create /private/preboot/cryptex1 in the Preboot volume (vol0) of root2.big.img so
# libignition's cryptex1 sniff (fstatat "cryptex1") returns 0 instead of ENOENT->8.
# qemu must be down. Run as root.
set -e
IMG=/home/ard/vrwork/root2.big.img
killall -9 qemu-system-aarch64 2>/dev/null || true; sleep 1
grep -q '^apfs ' /proc/modules || insmod /home/ard/kbuild/apfs/apfs.ko
L=$(losetup --show -f -o 1048576 "$IMG"); M=$(mktemp -d)
trap 'umount -q "$M" 2>/dev/null||true; losetup -d "$L" 2>/dev/null||true; rmdir "$M" 2>/dev/null||true' EXIT
mount -t apfs -o readwrite,vol=0 "$L" "$M"
echo "=== vol0 (Preboot) before ==="; ls -la "$M"
mkdir -p "$M/cryptex1"
sync
echo "=== vol0 after ==="; ls -la "$M"
echo "cryptex1 created: $(ls -ld "$M/cryptex1")"
