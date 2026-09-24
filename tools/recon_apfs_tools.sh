#!/bin/bash
# What apfs tooling exists, apfs module features, and vol=0 (Preboot) layout/space.
set -u
echo "=== apfs kernel module ==="; modinfo /home/ard/kbuild/apfs/apfs.ko 2>/dev/null | grep -iE 'version|resize|filename|description' | head
echo "=== apfsprogs binaries on PATH ==="; for t in mkapfs apfsck apfs-snap apfs-label resize.apfs apfs_resize; do command -v $t && $t 2>&1 | head -1; done
echo "=== apfs-related bins ==="; ls -la /home/ard/kbuild 2>/dev/null; find /home/ard -maxdepth 3 -iname 'mkapfs' -o -iname 'apfsck' 2>/dev/null | head
HYB=/home/ard/vrwork/root2.hybrid.img
grep -q '^apfs ' /proc/modules || insmod /home/ard/kbuild/apfs/apfs.ko
LH=$(losetup --show -f -o 1048576 "$HYB"); M0=$(mktemp -d)
trap 'umount -q "$M0" 2>/dev/null||true; losetup -d "$LH" 2>/dev/null||true; rmdir "$M0" 2>/dev/null||true' EXIT
echo "=== vol=0 (Preboot) ==="
mount -t apfs -o ro,vol=0 "$LH" "$M0" && { df -h "$M0" | tail -1; echo "--- top ---"; ls -la "$M0" | head; echo "--- any Cryptexes? ---"; find "$M0" -maxdepth 3 -iname 'Cryptex*' 2>/dev/null | head; echo "--- boot store ---"; ls -la "$M0"/boot/*/ 2>/dev/null | head -30; }
echo "=== apfs volumes in container (dump-apfs if present) ==="
command -v dump-apfs >/dev/null && dump-apfs "$LH" 2>/dev/null | grep -iE 'volume|role|APSB' | head -20 || echo "(no dump-apfs)"
