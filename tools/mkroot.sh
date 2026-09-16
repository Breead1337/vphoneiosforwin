#!/bin/bash
# root disk for vresearch101: GPT + one APFS container partition (mkapfs from apfsprogs), sparse
# volumes: 0 Preboot (role 0x10, iBoot mounts it at /boot), 1 System (role 0x1, sealed root hash lookup)
# mkapfs = apfsprogs patched by tools/apfsprogs_multivol.py (stock mkapfs makes one volume)
# usage (root; apfs.ko from tools/build_apfs_module.sh): bash mkroot.sh out.img [sizeG=16] [preboot-dir]
set -e; PATH=$PATH:/usr/sbin
out=$1; size=${2:-16}; tree=$3
rm -f "$out" "$out.apfs"
truncate -s ${size}G "$out"
sgdisk -Z -n 1:40:0 -t 1:7C3457EF-0000-11AA-AA11-00306543ECAC -c 1:Container "$out" >/dev/null
start=$(sgdisk -i 1 "$out" | awk '/First sector/{print $3}')
end=$(sgdisk -i 1 "$out" | awk '/Last sector/{print $3}')
truncate -s $(( (end - start + 1) * 512 )) "$out.apfs"
MK=${MKAPFS:-/home/ard/kbuild/apfsprogs/mkapfs/mkapfs}
$MK -L Preboot "$out.apfs"
if [ -n "$tree" ]; then
  grep -q "^apfs " /proc/modules || insmod ${APFS_KO:-/home/ard/kbuild/apfs/apfs.ko}
  mnt=$(mktemp -d)
  mount -t apfs -o loop,readwrite "$out.apfs" "$mnt"
  cp -r "$tree"/. "$mnt"/
  sync; umount "$mnt"; rmdir "$mnt"
fi
apfsck "$out.apfs" && echo apfsck-ok
dd if="$out.apfs" of="$out" bs=1M seek=$((start * 512)) oflag=seek_bytes conv=notrunc,sparse status=none
rm "$out.apfs"
sgdisk -p "$out" | tail -3
