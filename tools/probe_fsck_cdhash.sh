#!/bin/bash
# Extract fsck (and xpcproxy) from the image, compute cdhash, check membership in merged4.
set -e
IMG=/home/ard/vrwork/root2.big.img
killall -9 qemu-system-aarch64 2>/dev/null || true; sleep 1
losetup -D 2>/dev/null || true
grep -q '^apfs ' /proc/modules || insmod /home/ard/kbuild/apfs/apfs.ko
L=$(losetup --show -f -o 1048576 "$IMG"); M=$(mktemp -d)
trap 'umount -q "$M" 2>/dev/null||true; losetup -d "$L" 2>/dev/null||true; rmdir "$M" 2>/dev/null||true' EXIT
mount -t apfs -o ro,vol=1 "$L" "$M"
for b in /sbin/fsck /usr/libexec/xpcproxy; do
  cp "$M$b" "/home/ard/vrwork/$(basename $b).bin"
done
umount "$M"; losetup -d "$L"; rmdir "$M"; trap - EXIT
python3 - <<'PY'
import struct, hashlib
def cdhash(path):
    d=open(path,'rb').read()
    if d[:4]!=b'\xcf\xfa\xed\xfe': return None
    ncmds=struct.unpack_from('<I',d,16)[0]; p=32; cs=None
    for _ in range(ncmds):
        cmd,sz=struct.unpack_from('<II',d,p)
        if cmd==0x1d: cs=struct.unpack_from('<II',d,p+8)
        p+=sz
    if not cs: return 'no-LC_CODE_SIGNATURE'
    blob=d[cs[0]:cs[0]+cs[1]]; mg,ln,n=struct.unpack_from('>III',blob,0)
    for i in range(n):
        t,off=struct.unpack_from('>II',blob,12+i*8)
        if struct.unpack_from('>I',blob,off)[0]==0xfade0c02:
            L=struct.unpack_from('>I',blob,off+4)[0]
            return hashlib.sha256(blob[off:off+L]).digest()[:20].hex()
    return 'no-CD'
tc=open('/mnt/d/vphonewin/_work/tc/merged4.trst.bin','rb').read()
ver,uuid,n=struct.unpack_from('<I16sI',tc,0); stride=(len(tc)-24)//n
s={tc[24+i*stride:24+i*stride+20] for i in range(n)}
for b in ['fsck','xpcproxy']:
    h=cdhash('/home/ard/vrwork/%s.bin'%b)
    inn = bytes.fromhex(h) in s if h and len(h)==40 else '?'
    print('%-10s cdhash=%s inTC=%s' % (b,h,inn))
PY
