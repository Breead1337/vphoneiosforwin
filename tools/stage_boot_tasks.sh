#!/bin/bash
# stage_boot_tasks.sh — session 50. Ставит "fake exit-0" стабы в места где
# launchd hardwired ищет boot tasks:
#   /usr/libexec/MSUEarlyBootTask
#   /usr/libexec/MobileAssetEarlyBootTask
#   /System/Library/PrivateFrameworks/MobileAccessoryUpdater.framework/Support/auearlyboot
# (darwinos-boot-task путь неизвестен — если понадобится, добавим позже).
#
# Каждый стаб = копия /sbin/fsck с патчем LC_MAIN entry на `mov w0,#0; ret`
# и пересчитанным CDHash (adhoc CS blob). CDHash добавляется в TC blob,
# который потом попадает в guest RAM через $VR_TRUSTCACHE + DT.
#
# usage (в WSL с sudo): sudo bash /mnt/d/vphonewin/tools/stage_boot_tasks.sh
set -e
ROOT=/mnt/d/vphonewin
IMG=${IMG:-/home/${SUDO_USER:-ard}/vrwork/root2.img}
TC=${TC:-$ROOT/_work/tc/os.trst.bin}
KO=${APFS_KO:-/home/ard/kbuild/apfs/apfs.ko}

grep -q '^apfs ' /proc/modules || insmod "$KO"
LOOP=$(losetup -f)
losetup -o 1048576 "$LOOP" "$IMG"
MNT=$(mktemp -d)
trap 'umount -q "$MNT" || true; losetup -d "$LOOP"; rmdir "$MNT" 2>/dev/null || true' EXIT
mount -t apfs -o readwrite,vol=1 "$LOOP" "$MNT"

# Sources: fsck на диске (может быть stubbed от прошлого stub_fsck; берём чистый если есть)
SRC="$MNT/sbin/fsck"
[ -f "$SRC" ] || { echo "нет $SRC"; exit 1; }

WORK=$(mktemp -d)
STUB="$WORK/stub"
CDHASH=$(python3 "$ROOT/tools/patch_cs.py" "$SRC" "$STUB" | awk '{print $NF}')
echo "стаб готов, CDHash=$CDHASH"

# Ставим в 4 patha (owner+mode как оригинал fsck: r-xr-xr-x root)
for dst in \
    /usr/libexec/MSUEarlyBootTask \
    /usr/libexec/MobileAssetEarlyBootTask \
    /System/Library/PrivateFrameworks/MobileAccessoryUpdater.framework/Support/auearlyboot ; do
    mkdir -p "$(dirname "$MNT$dst")"
    cp "$STUB" "$MNT$dst"
    chmod 555 "$MNT$dst"
    chown 0:0 "$MNT$dst"
    echo "  → $dst"
done

sync
umount "$MNT"

# Добавляем CDHash в TC (один раз — все 4 стаба одинаковые, значит один CDHash)
python3 "$ROOT/tools/tc_append.py" "$TC" "$CDHASH"

rm -rf "$WORK"
echo "OK"
