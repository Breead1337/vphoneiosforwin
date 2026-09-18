#!/bin/bash
set -e
mkdir -p /tmp/v0 /tmp/v1
losetup -d /dev/loop11 2>/dev/null || true
losetup -o 1048576 /dev/loop11 /home/ard/vrwork/root2.img
mount -t apfs -o ro,vol=0 /dev/loop11 /tmp/v0 2>&1 || true
mount -t apfs -o ro,vol=1 /dev/loop11 /tmp/v1 2>&1 || true

echo "=== Volume 0 ==="
ls -la /tmp/v0 || true

echo "=== Volume 1 ==="
ls -la /tmp/v1 || true

umount /tmp/v0 2>/dev/null || true
umount /tmp/v1 2>/dev/null || true
losetup -d /dev/loop11 2>/dev/null || true
