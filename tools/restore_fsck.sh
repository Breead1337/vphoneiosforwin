#!/bin/bash
# Восстановить /sbin/fsck из чистого backup ~/vrwork/root2.bak.img в текущий root2.img.
# Нужен если stage_boot_tasks stubbed fsck (сессия 52 узнала что stub fsck ломает
# path/ident invariant в AMFI, оригинальный fsck CDHash уже в TC).
set -e
KO=${APFS_KO:-/home/ard/kbuild/apfs/apfs.ko}
IMG=/home/${SUDO_USER:-ard}/vrwork/root2.img
SRC=/mnt/d/vphonewin/fw/cloud/raw/fsck.bin  # оригинал md5 5ae828fa...
grep -q '^apfs ' /proc/modules || insmod "$KO"

LOOP=$(losetup -f)
losetup -o 1048576 "$LOOP" "$IMG"
MNT=$(mktemp -d)
mount -t apfs -o readwrite,vol=1 "$LOOP" "$MNT"

cp "$SRC" "$MNT/sbin/fsck"
chmod 555 "$MNT/sbin/fsck"
chown 0:0 "$MNT/sbin/fsck"
md5sum "$MNT/sbin/fsck" "$SRC"

sync
umount "$MNT"; rmdir "$MNT"; losetup -d "$LOOP"
echo "fsck restored"
