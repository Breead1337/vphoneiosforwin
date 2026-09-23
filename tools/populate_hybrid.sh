#!/bin/bash
# Replace root2.hybrid.img System volume (vol=1) contents with the iPhone OS
# filesystem (SpringBoard/UIKit). Working root2.img is never touched.
set -e
modprobe loop 2>/dev/null
grep -q "^apfs " /proc/modules || insmod /home/ard/kbuild/apfs/apfs.ko
DMG=/home/ard/vrwork/iphone_os/043-53486-120.dmg
HYB=/home/ard/vrwork/root2.hybrid.img
mkdir -p /tmp/src /tmp/dst
# source: iPhone OS System volume (ro)
LS=$(losetup --find --show "$DMG")
mount -t apfs -o ro,vol=0 "$LS" /tmp/src
# dest: hybrid System volume (rw)
LD=$(losetup --find --show -o 1048576 "$HYB")
mount -t apfs -o readwrite,vol=1 "$LD" /tmp/dst
echo "=== wiping old cloudOS rootfs in hybrid vol=1 ==="
# keep the mnt* mountpoints, remove everything else
( cd /tmp/dst && rm -rf bin cores etc Library private sbin System tmp usr var Applications Developer 2>/dev/null || true )
echo "=== copying iPhone OS ($(du -sh /tmp/src 2>/dev/null | cut -f1)) into hybrid vol=1 ==="
time cp -a /tmp/src/. /tmp/dst/ 2>&1 | tail -3 || true
sync
echo "=== result top of hybrid vol=1 ==="
ls /tmp/dst | head -20
echo "=== SpringBoard present in hybrid? ==="
ls -la /tmp/dst/System/Library/CoreServices/SpringBoard.app/SpringBoard 2>&1
umount /tmp/dst 2>/dev/null; umount /tmp/src 2>/dev/null
losetup -d "$LD" 2>/dev/null; losetup -d "$LS" 2>/dev/null
rmdir /tmp/dst /tmp/src 2>/dev/null
echo DONE
