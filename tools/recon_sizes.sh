#!/bin/bash
# Read-only sizing recon for the dyld-cache placement plan. qemu MUST be down.
set -u
echo "qemu procs: $(ps -C qemu-system-aar --no-headers | wc -l)"
HYB=/home/ard/vrwork/root2.hybrid.img
CRY=/home/ard/vrwork/cryptex/043-54303-126.dmg
echo "=== image file on disk ==="; ls -la "$HYB" "$CRY" 2>/dev/null
echo "=== host free (vrwork fs) ==="; df -h /home/ard/vrwork | tail -2
grep -q '^apfs ' /proc/modules || insmod /home/ard/kbuild/apfs/apfs.ko

LC=$(losetup --show -f "$CRY"); MC=$(mktemp -d)
LH=$(losetup --show -f -o 1048576 "$HYB"); MH=$(mktemp -d)
cleanup(){ umount -q "$MC" 2>/dev/null||true; umount -q "$MH" 2>/dev/null||true; losetup -d "$LC" 2>/dev/null||true; losetup -d "$LH" 2>/dev/null||true; rmdir "$MC" "$MH" 2>/dev/null||true; }
trap cleanup EXIT
mount -t apfs -o ro,vol=0 "$LC" "$MC"
mount -t apfs -o ro,vol=1 "$LH" "$MH"

echo "=== cryptex dyld cache: all subcaches + total ==="
ls -la "$MC/System/Library/Caches/com.apple.dyld/" | grep -i dyld_shared_cache
echo "--- count + total bytes ---"
du -sh "$MC/System/Library/Caches/com.apple.dyld/" 2>/dev/null
find "$MC/System/Library/Caches/com.apple.dyld/" -iname 'dyld_shared_cache_arm64e*' | wc -l

echo "=== rootfs (System vol=1) free ==="; df -h "$MH" | tail -1
echo "=== rootfs cryptex/symlink layout ==="
ls -ld "$MH/System/Cryptexes" "$MH/System/Cryptexes/OS" 2>/dev/null || echo "(no /System/Cryptexes)"
ls -ld "$MH/private/preboot/Cryptexes" "$MH/private/preboot/Cryptexes/OS" 2>/dev/null || echo "(no /private/preboot/Cryptexes)"
ls -la "$MH/System/Library/Caches/com.apple.dyld/" 2>/dev/null || echo "(no /System/Library/Caches/com.apple.dyld)"
echo "=== leftover from de-risk at graft point ==="
ls -la "$MH/private/preboot/Cryptexes/OS/System/Library/Caches/com.apple.dyld/" 2>/dev/null || echo "(none)"
