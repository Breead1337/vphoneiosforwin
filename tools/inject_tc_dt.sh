#!/bin/bash
# Инжектит патченный DeviceTree (с /chosen/memory-map/TrustCache) в Preboot-том root2.img.
# Требует sudo для insmod apfs.ko + losetup + mount -t apfs.
#
# usage (в WSL, ОДИН РАЗ с паролем):
#   sudo bash /mnt/d/vphonewin/tools/inject_tc_dt.sh
#
# Что делает: пересобирает DT через tools/dtpatch.py с VR_TRUSTCACHE,
# монтирует Volume 0 (Preboot) в ~/vrwork/root2.img, заменяет
# /{NSIH}/usr/standalone/firmware/devicetree.img4, umount.
set -e
ROOT=/mnt/d/vphonewin
# под sudo $HOME становится /root; берём владельца скрипта, т.е. реального юзера WSL.
REAL_HOME=${SUDO_USER:+/home/$SUDO_USER}
IMG=${IMG:-${REAL_HOME:-$HOME}/vrwork/root2.img}
TC=${TC:-$ROOT/_work/tc/os.trst.bin}
DT_OUT=$ROOT/fw/cloud/DeviceTree.patched.im4p
KO=${APFS_KO:-/home/ard/kbuild/apfs/apfs.ko}

[ -f "$TC" ] || { echo "нет $TC — сначала: $ROOT/tools/ipsw.exe img4 im4p extract -o $TC $ROOT/fw/cloud/Firmware/094-39278-029.dmg.aea.trustcache"; exit 1; }
[ -f "$IMG" ] || { echo "нет $IMG"; exit 1; }
[ -f "$KO" ] || { echo "нет $KO — собери: bash $ROOT/tools/build_apfs_module.sh"; exit 1; }

VR_TRUSTCACHE="$TC" VR_BOOTARGS="${VR_BOOTARGS:-cs_enforcement_disable=1 amfi_get_out_of_my_way=1 debug=0x14e -v}" \
  python3 "$ROOT/tools/dtpatch.py" "$DT_OUT"

grep -q '^apfs ' /proc/modules || insmod "$KO"

LOOP=$(losetup -f)
losetup -o 1048576 "$LOOP" "$IMG"
trap 'umount -q "$MNT" || true; losetup -d "$LOOP"; rmdir "$MNT" 2>/dev/null || true' EXIT

MNT=$(mktemp -d)
mount -t apfs -o readwrite,vol=0 "$LOOP" "$MNT"

NSIH=$(cat "$MNT/active" | tr -d '[:space:]')
[ -n "$NSIH" ] || { echo "не нашёл /active"; exit 1; }
DST="$MNT/$NSIH/usr/standalone/firmware/devicetree.img4"
mkdir -p "$(dirname "$DST")"

# IMG4 wrapper (mkaux.img4()) — тот же формат что mkpreboot.py делает
python3 - "$DT_OUT" "$DST" <<'PY'
import sys
sys.path.insert(0, "/mnt/d/vphonewin/tools")
from mkaux import img4
open(sys.argv[2], "wb").write(img4(open(sys.argv[1], "rb").read()))
print(f"wrote {sys.argv[2]}")
PY

sync
echo "OK: devicetree.img4 заменён на Preboot (NSIH=$NSIH)"
