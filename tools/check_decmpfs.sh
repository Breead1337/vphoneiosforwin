#!/bin/bash
# Check whether spawned binaries (fsck) are valid Mach-O on the System volume or garbage
# (decmpfs xattr present but data uncompressed = corruption from cp -a). qemu down. root.
set -e
IMG=/home/ard/vrwork/root2.big.img
killall -9 qemu-system-aarch64 2>/dev/null || true; sleep 1
losetup -D 2>/dev/null || true
grep -q '^apfs ' /proc/modules || insmod /home/ard/kbuild/apfs/apfs.ko
L=$(losetup --show -f -o 1048576 "$IMG"); M=$(mktemp -d)
trap 'umount -q "$M" 2>/dev/null||true; losetup -d "$L" 2>/dev/null||true; rmdir "$M" 2>/dev/null||true' EXIT
mount -t apfs -o ro,vol=1 "$L" "$M"
for f in /sbin/fsck /sbin/fsck_apfs /sbin/launchd /usr/lib/dyld /bin/ls /usr/libexec/xpcproxy; do
  p="$M$f"
  if [ -e "$p" ]; then
    sz=$(stat -c %s "$p" 2>/dev/null)
    mg=$(head -c4 "$p" 2>/dev/null | od -An -tx1 | tr -d ' \n')
    dc=$(getfattr -n com.apple.decmpfs --only-values "$p" 2>/dev/null | head -c16 | od -An -tx1 | tr -d ' \n' || echo "none")
    printf "%-24s size=%-9s magic=%-8s decmpfs=%s\n" "$f" "$sz" "$mg" "${dc:-none}"
  else
    printf "%-24s (absent)\n" "$f"
  fi
done
echo "--- xattr list on fsck ---"; getfattr -d -m - "$M/sbin/fsck" 2>/dev/null | head
