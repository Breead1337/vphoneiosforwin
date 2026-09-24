#!/bin/bash
# dyld_v5 = clean dyld + two patches, re-signed:
#   0x7d98c: NOP        (graft-stage tbz -> optional; keeps ignition passing)
#   0x63c94: b 0x62c10  (redirect mapSplitCacheSystemWide -> mapSplitCachePrivate so
#                        spawned children map the cache from file instead of inheriting
#                        the empty kernel shared region)
# Then merged5 TC + StaticTrustCache + apply. qemu down. root.
set -e
W=/home/ard/vrwork; TCDIR=/mnt/d/vphonewin/_work/tc; IMG=$W/root2.big.img
killall -9 qemu-system-aarch64 2>/dev/null || true; sleep 1; losetup -D 2>/dev/null || true

echo "=== [1] compute branch bytes for b 0x62c10 @ 0x63c94 ==="
python3 - <<'PY'
tgt=0x62c10; src=0x63c94; off=(tgt-src)//4
instr=0x14000000 | (off & 0x03ffffff)
import struct
print("branch instr=0x%08x bytes=%s" % (instr, struct.pack('<I',instr).hex()))
open('/tmp/br.hex','w').write(struct.pack('<I',instr).hex())
PY
BR=$(cat /tmp/br.hex)

echo "=== [2] patch + re-sign (dyld_v5) ==="
python3 /mnt/d/vphonewin/tools/resign_dyld.py "$W/dyld_hybrid" "$W/dyld_v5" "0x7d98c:1f2003d5" "0x63c94:$BR"
NEWCD=$(cat "$W/dyld_v5.cdhash")

echo "=== [3] verify patched bytes ==="
python3 -c "d=open('/home/ard/vrwork/dyld_v5','rb').read(); print('0x63c94=',d[0x63c94:0x63c98].hex(),'(want dffbff17)'); print('0x7d98c=',d[0x7d98c:0x7d990].hex(),'(want 1f2003d5)')"

echo "=== [4] merged5 + StaticTrustCache + inject ==="
cp "$TCDIR/merged2.trst.bin" "$TCDIR/merged5.trst.bin"
python3 /mnt/d/vphonewin/tools/tc_append.py "$TCDIR/merged5.trst.bin" "$NEWCD"
python3 /mnt/d/vphonewin/tools/build_static_tc.py "$TCDIR/merged5.trst.bin" "$W/static_tc_v5.img4"
IMG="$IMG" NEW="$W/static_tc_v5.img4" bash /mnt/d/vphonewin/tools/inject_static_tc.sh

echo "=== [5] apply dyld_v5 ==="
grep -q '^apfs ' /proc/modules || insmod /home/ard/kbuild/apfs/apfs.ko
L=$(losetup --show -f -o 1048576 "$IMG"); M=$(mktemp -d)
trap 'umount -q "$M" 2>/dev/null||true; losetup -d "$L" 2>/dev/null||true; rmdir "$M" 2>/dev/null||true' EXIT
mount -t apfs -o readwrite,vol=1 "$L" "$M"
rm -f "$M/usr/lib/dyld"; cp "$W/dyld_v5" "$M/usr/lib/dyld"; chmod 0755 "$M/usr/lib/dyld"; sync
umount "$M"; losetup -d "$L"; rmdir "$M"; trap - EXIT
chown ard:ard "$IMG"
echo "DONE. Boot TC=$TCDIR/merged5.trst.bin"
