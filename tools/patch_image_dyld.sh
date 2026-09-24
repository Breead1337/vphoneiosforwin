#!/bin/bash
# Patch /usr/lib/dyld in root2.big.img (System vol) to NOP the graft-os fatal branch.
# Replaces the file (rm+cp) to avoid stale decmpfs xattr. qemu must be down. root.
set -e
IMG=/home/ard/vrwork/root2.big.img
SRC=/home/ard/vrwork/dyld_hybrid
PATCHED=/home/ard/vrwork/dyld_patched
killall -9 qemu-system-aarch64 2>/dev/null || true; sleep 1
losetup -D 2>/dev/null || true
cp "$SRC" "$PATCHED"
python3 /mnt/d/vphonewin/tools/patch_dyld_cryptex.py "$PATCHED" --apply
grep -q '^apfs ' /proc/modules || insmod /home/ard/kbuild/apfs/apfs.ko
L=$(losetup --show -f -o 1048576 "$IMG"); M=$(mktemp -d)
trap 'umount -q "$M" 2>/dev/null||true; losetup -d "$L" 2>/dev/null||true; rmdir "$M" 2>/dev/null||true' EXIT
mount -t apfs -o readwrite,vol=1 "$L" "$M"
echo "old dyld: $(stat -c %s "$M/usr/lib/dyld") bytes"
rm -f "$M/usr/lib/dyld"
cp "$PATCHED" "$M/usr/lib/dyld"
chmod 0755 "$M/usr/lib/dyld"
sync
echo "new dyld: $(stat -c %s "$M/usr/lib/dyld") bytes; patched byte:"
python3 -c "d=open('$M/usr/lib/dyld','rb').read(); print(' 0x7e1a8 =', d[0x7e1a8:0x7e1ac].hex())"
umount "$M"; losetup -d "$L"; rmdir "$M"; trap - EXIT
chown ard:ard "$IMG"
echo DONE
