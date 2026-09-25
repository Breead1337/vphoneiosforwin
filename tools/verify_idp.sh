#!/bin/bash
IMG=/home/ard/vrwork/root2.big.img
grep -q '^apfs ' /proc/modules || insmod /home/ard/kbuild/apfs/apfs.ko
LOOP=$(losetup -f); losetup -o 1048576 "$LOOP" "$IMG"
MNT=$(mktemp -d)
trap 'umount -q "$MNT" 2>/dev/null||true; losetup -d "$LOOP" 2>/dev/null||true; rmdir "$MNT" 2>/dev/null||true' EXIT
mount -t apfs -o ro,vol=1 "$LOOP" "$MNT"
echo "=== init_data_protection symlink ==="; ls -la "$MNT/usr/libexec/init_data_protection"; readlink "$MNT/usr/libexec/init_data_protection"
echo "=== seputil ==="; ls -la "$MNT/usr/libexec/seputil"
echo "=== seputil patched byte @0x3b18 (expect 000080d2) ==="
python3 -c "f=open(\"$MNT/usr/libexec/seputil\",\"rb\").read(); print(f[0x3b18:0x3b1c].hex()); print(\"size\",len(f))"
