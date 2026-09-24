#!/bin/bash
# Reset apfsprogs, re-apply the (now 6-volume) multivol patch, rebuild mkapfs,
# then make a small test container and validate with apfsck + mount all 6 volumes.
set -e
AP=/home/ard/kbuild/apfsprogs
KO=/home/ard/kbuild/apfs/apfs.ko
echo "=== reset apfsprogs to pristine ==="
git -C "$AP" checkout -- . 2>&1 | tail -2 || true
echo "=== apply 6-volume patch ==="
python3 /mnt/d/vphonewin/tools/apfsprogs_multivol.py "$AP"
echo "=== rebuild mkapfs ==="
make -C "$AP/mkapfs" 2>&1 | tail -5
MK="$AP/mkapfs/mkapfs"
echo "=== small test container ==="
T=/tmp/t6.apfs
rm -f "$T"; truncate -s 4G "$T"
"$MK" -L Preboot "$T"
echo "=== apfsck (must be clean; 4G => max_vols=8 >= 6) ==="
CK=$("$AP/apfsck/apfsck" "$T" 2>&1); echo "$CK" | tail -8
echo "$CK" | grep -qiE 'too many|error|corrupt|invalid|fail' && echo "APFSCK-PROBLEM" || echo "APFSCK-CLEAN"
echo "=== mount all 6 volumes ro, show role/name ==="
grep -q '^apfs ' /proc/modules || insmod "$KO"
L=$(losetup --show -f "$T")
for v in 0 1 2 3 4 5; do
  M=$(mktemp -d)
  if mount -t apfs -o ro,vol=$v "$L" "$M" 2>/dev/null; then
    echo "vol$v: mounted OK ($(ls -a "$M" | tr '\n' ' '))"
    umount "$M"
  else
    echo "vol$v: MOUNT FAILED"
  fi
  rmdir "$M"
done
losetup -d "$L"
echo DONE
