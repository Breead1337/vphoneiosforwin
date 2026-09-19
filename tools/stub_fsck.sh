#!/bin/bash
# Стаб /sbin/fsck на System volume (Vol 1) в root2.img: entry @0x92c → `mov w0,#0 ; ret`.
# После session 41 fsck запускается, но падает с SIGKILL внутри libc/dyld (wild pointer
# 0xd00cc0000 — session 42-в исследовании). Пока корень не найден — обходим весь fsck,
# чтобы launchd мог продолжить boot chain и мы увидели следующий шаг.
#
# usage (в WSL с sudo): sudo bash /mnt/d/vphonewin/tools/stub_fsck.sh
set -e
IMG=${IMG:-/home/${SUDO_USER:-ard}/vrwork/root2.img}
KO=${APFS_KO:-/home/ard/kbuild/apfs/apfs.ko}
grep -q '^apfs ' /proc/modules || insmod "$KO"
LOOP=$(losetup -f)
losetup -o 1048576 "$LOOP" "$IMG"
MNT=$(mktemp -d)
trap 'umount -q "$MNT" || true; losetup -d "$LOOP"; rmdir "$MNT" 2>/dev/null || true' EXIT
mount -t apfs -o readwrite,vol=1 "$LOOP" "$MNT"

python3 - "$MNT/sbin/fsck" <<'PY'
import struct, sys
p = sys.argv[1]
d = bytearray(open(p, "rb").read())
# LC_MAIN entryoff = 0x92c (см. `otool -l /sbin/fsck | grep -A2 LC_MAIN`, session 36):
#   0x52800000 = mov w0, #0
#   0xd65f03c0 = ret
patch = struct.pack("<II", 0x52800000, 0xd65f03c0)
cur = bytes(d[0x92c:0x92c+8])
if cur == patch:
    print("fsck: already stubbed (@0x92c)")
else:
    d[0x92c:0x92c+8] = patch
    open(p, "wb").write(d)
    print(f"fsck: stubbed @0x92c (was {cur.hex()})")
PY
sync
echo "OK"
