#!/bin/bash
# Restore UNPATCHED dyld_hybrid into root2.big.img (same rm+cp method) to isolate cause.
set -e
IMG=/home/ard/vrwork/root2.big.img
SRC=/home/ard/vrwork/dyld_hybrid
killall -9 qemu-system-aarch64 2>/dev/null || true; sleep 1
losetup -D 2>/dev/null || true
grep -q '^apfs ' /proc/modules || insmod /home/ard/kbuild/apfs/apfs.ko
L=$(losetup --show -f -o 1048576 "$IMG"); M=$(mktemp -d)
trap 'umount -q "$M" 2>/dev/null||true; losetup -d "$L" 2>/dev/null||true; rmdir "$M" 2>/dev/null||true' EXIT
mount -t apfs -o readwrite,vol=1 "$L" "$M"
rm -f "$M/usr/lib/dyld"; cp "$SRC" "$M/usr/lib/dyld"; chmod 0755 "$M/usr/lib/dyld"
sync
python3 -c "d=open('$M/usr/lib/dyld','rb').read(); print('0x7e1a8 =', d[0x7e1a8:0x7e1ac].hex(), '(expect 97e2ff35 unpatched)')"
umount "$M"; losetup -d "$L"; rmdir "$M"; trap - EXIT
chown ard:ard "$IMG"
echo DONE
