#!/bin/bash
# Полное обновление Preboot volume (Vol 0) в root2.img: пересобирает DT
# (dtpatch.py + $VR_TRUSTCACHE) и подставляет patched kernelcache
# (см. tools/patch_kc.py). Использует tools/mkpreboot.py как источник
# формата IMG4 обёртки.
#
# usage (в WSL с sudo): sudo bash /mnt/d/vphonewin/tools/stage_preboot.sh
set -e
ROOT=/mnt/d/vphonewin
IMG=${IMG:-/home/${SUDO_USER:-ard}/vrwork/root2.img}
TC=${TC:-$ROOT/_work/tc/os.trst.bin}
KO=${APFS_KO:-/home/ard/kbuild/apfs/apfs.ko}

[ -f "$TC" ]  || { echo "no $TC (ipsw img4 im4p extract сначала)"; exit 1; }
[ -f "$IMG" ] || { echo "no $IMG"; exit 1; }
[ -f "$KO" ]  || { echo "no $KO (build_apfs_module.sh)"; exit 1; }
[ -f "$ROOT/fw/cloud/kernelcache.patched.im4p" ] || {
    echo "no kernelcache.patched.im4p — запусти tools/patch_kc.py сначала"; exit 1; }

VR_TRUSTCACHE="$TC" VR_BOOTARGS="${VR_BOOTARGS:-}" \
  python3 "$ROOT/tools/dtpatch.py" "$ROOT/fw/cloud/DeviceTree.patched.im4p"

STAGE=$(mktemp -d)
python3 "$ROOT/tools/mkpreboot.py" "$STAGE"

grep -q '^apfs ' /proc/modules || insmod "$KO"
LOOP=$(losetup -f)
losetup -o 1048576 "$LOOP" "$IMG"
MNT=$(mktemp -d)
trap 'umount -q "$MNT" || true; losetup -d "$LOOP"; rmdir "$MNT" 2>/dev/null || true; rm -rf "$STAGE"' EXIT
mount -t apfs -o readwrite,vol=0 "$LOOP" "$MNT"

NSIH=$(cat "$MNT/active" | tr -d '[:space:]')
[ -n "$NSIH" ] || { echo "нет /active"; exit 1; }

# Копируем весь стейджинг поверх Preboot (перезаписываем)
cp -av "$STAGE/$NSIH/." "$MNT/$NSIH/" | tail -20

sync
echo "OK: Preboot vol0 обновлён (NSIH=$NSIH)"
