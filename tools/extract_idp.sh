#!/bin/bash
# Mount the iPhone OS DMG (separate file, RO) and extract init_data_protection.
set -e
PW=Elite1337
IMG=/home/ard/vrwork/iphone_os/043-53486-120.dmg
KO=/home/ard/kbuild/apfs/apfs.ko
MNT=/tmp/idp_mnt
S() { echo "$PW" | sudo -S "$@" 2>/dev/null; }
grep -q '^apfs ' /proc/modules || S insmod "$KO"
mkdir -p "$MNT"
LOOP=$(echo "$PW" | sudo -S losetup -f 2>/dev/null)
# OS DMG is raw APFS at offset 0
S losetup "$LOOP" "$IMG"
for off in 0 1048576; do
  S losetup -d "$LOOP" 2>/dev/null || true
  S losetup -o $off "$LOOP" "$IMG"
  for v in 0 1 2; do
    if S mount -t apfs -o ro,vol=$v "$LOOP" "$MNT" 2>/dev/null; then
      if [ -e "$MNT/usr/libexec/init_data_protection" ]; then
        echo "FOUND at offset=$off vol=$v"
        S cp "$MNT/usr/libexec/init_data_protection" /home/ard/vrwork/init_data_protection
        S chmod 644 /home/ard/vrwork/init_data_protection
        S umount "$MNT"; S losetup -d "$LOOP"
        ls -la /home/ard/vrwork/init_data_protection
        exit 0
      fi
      S umount "$MNT" 2>/dev/null || true
    fi
  done
done
S losetup -d "$LOOP" 2>/dev/null || true
echo "NOT FOUND"
