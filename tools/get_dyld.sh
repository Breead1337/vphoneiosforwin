#!/bin/bash
set -e
grep -q '^apfs ' /proc/modules || insmod /home/ard/kbuild/apfs/apfs.ko
L=$(losetup --show -f -o 1048576 /home/ard/vrwork/root2.hybrid.img)
M=$(mktemp -d)
trap 'umount -q "$M" 2>/dev/null||true; losetup -d "$L" 2>/dev/null||true; rmdir "$M" 2>/dev/null||true' EXIT
mount -t apfs -o ro,vol=1 "$L" "$M"
ls -la "$M/usr/lib/dyld"
cp "$M/usr/lib/dyld" /home/ard/vrwork/dyld_hybrid
chmod 0666 /home/ard/vrwork/dyld_hybrid
echo "copied dyld $(stat -c %s /home/ard/vrwork/dyld_hybrid) bytes"
