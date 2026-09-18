#!/bin/bash
set -e
mkdir -p /mnt_sys
losetup -d /dev/loop15 2>/dev/null || true
losetup -o 1048576 /dev/loop15 /home/ard/vrwork/root2.img
mount -t apfs -o ro,vol=1 /dev/loop15 /mnt_sys
echo "=== Contents of root2.img Volume 1 (/mnt_sys) ==="
ls -la /mnt_sys
echo "Does /sbin/launchd exist?"
ls -la /mnt_sys/sbin/launchd 2>&1 || true
umount /mnt_sys
losetup -d /dev/loop15
