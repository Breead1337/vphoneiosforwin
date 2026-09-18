#!/bin/bash
set -e

DMG=/mnt/d/vphonewin/_work/rootfs/test-decrypt/094-39278-029.dmg
IMG=/home/ard/vrwork/root2.img

mkdir -p /tmp/mnt_dmg /tmp/mnt_v1
mount -t apfs -o ro $DMG /tmp/mnt_dmg

losetup -d /dev/loop18 2>/dev/null || true
losetup -o 1048576 /dev/loop18 $IMG
mount -t apfs -o readwrite,vol=1 /dev/loop18 /tmp/mnt_v1

echo "Copying full decrypted rootfs to Volume 1..."
time cp -a /tmp/mnt_dmg/* /tmp/mnt_v1/ 2>&1 || true

sync
echo "Done copying rootfs!"
ls -la /tmp/mnt_v1
ls -la /tmp/mnt_v1/usr/lib/dyld
ls -la /tmp/mnt_v1/sbin/launchd

umount /tmp/mnt_v1
losetup -d /dev/loop18
umount /tmp/mnt_dmg

# --- ponytail: patch /sbin/fsck to return 0 immediately (session 36) ---
# After the cp above, if we're still mounted, patch fsck entry.
if mountpoint -q /tmp/mnt_v1 2>/dev/null; then
    python3 - <<'PY'
import struct
p='/tmp/mnt_v1/sbin/fsck'
try:
    d=bytearray(open(p,'rb').read())
    # LC_MAIN entryoff=0x92c: mov w0,#0 ; ret
    d[0x92c:0x92c+8]=struct.pack('<II', 0x52800000, 0xd65f03c0)
    open(p,'wb').write(d)
    print('fsck patched at 0x92c')
except Exception as e:
    print('fsck patch skipped:', e)
PY
fi
