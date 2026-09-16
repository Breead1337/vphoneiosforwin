#!/bin/bash
# root disk for vresearch101: GPT + one APFS container partition (mkapfs from apfsprogs), sparse
# Preboot role is what iBoot fsboot mounts at /boot (FUN_700a2a74, role 0x10)
# usage: bash mkroot.sh out.img [sizeG=16]
set -e; PATH=$PATH:/usr/sbin
out=$1; size=${2:-16}
rm -f "$out" "$out.apfs"
truncate -s ${size}G "$out"
sgdisk -Z -n 1:40:0 -t 1:7C3457EF-0000-11AA-AA11-00306543ECAC -c 1:Container "$out" >/dev/null
start=$(sgdisk -i 1 "$out" | awk '/First sector/{print $3}')
end=$(sgdisk -i 1 "$out" | awk '/Last sector/{print $3}')
truncate -s $(( (end - start + 1) * 512 )) "$out.apfs"
mkapfs -L Preboot "$out.apfs"
python3 /mnt/d/vphonewin/tools/apfs_role.py "$out.apfs" 0x10   # iBoot mounts /boot by role Preboot
apfsck "$out.apfs" && echo apfsck-ok
dd if="$out.apfs" of="$out" bs=1M seek=$((start * 512)) oflag=seek_bytes conv=notrunc,sparse status=none
rm "$out.apfs"
sgdisk -p "$out" | tail -3
