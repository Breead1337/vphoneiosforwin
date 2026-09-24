#!/bin/bash
# dyld_v6: PID-conditional trampoline so launchd (PID 1) keeps system-wide cache
# mapping while spawned children fall back to private mapping.
#   0x63c94: b 0x51a8   (systemwide entry -> stub)
#   0x51a8 : stub (getpid; if !=1 -> b 0x62c10 private; else pacibsp; b 0x63c98)
#   0x7d98c: NOP        (graft-stage optional; keep ignition passing)
set -e
W=/home/ard/vrwork; TCDIR=/mnt/d/vphonewin/_work/tc; IMG=$W/root2.big.img
killall -9 qemu-system-aarch64 2>/dev/null || true; sleep 1; losetup -D 2>/dev/null || true
STUB=e007bfa9900280d2011000d41f0400f1e007c1a8a1d22e547f2303d5b57a0114
echo "=== [1] patch + re-sign (dyld_v6) ==="
python3 /mnt/d/vphonewin/tools/resign_dyld.py "$W/dyld_hybrid" "$W/dyld_v6" \
  "0x7d98c:1f2003d5" "0x63c94:4585fe17" "0x51a8:$STUB"
NEWCD=$(cat "$W/dyld_v6.cdhash")
echo "=== [2] verify patched bytes ==="
python3 -c "d=open('$W/dyld_v6','rb').read();print('0x63c94=',d[0x63c94:0x63c98].hex());print('0x51a8=',d[0x51a8:0x51c8].hex());print('0x7d98c=',d[0x7d98c:0x7d990].hex())"
echo "=== [3] merged6 + StaticTrustCache + inject ==="
cp "$TCDIR/merged2.trst.bin" "$TCDIR/merged6.trst.bin"
python3 /mnt/d/vphonewin/tools/tc_append.py "$TCDIR/merged6.trst.bin" "$NEWCD"
python3 /mnt/d/vphonewin/tools/build_static_tc.py "$TCDIR/merged6.trst.bin" "$W/static_tc_v6.img4"
IMG="$IMG" NEW="$W/static_tc_v6.img4" bash /mnt/d/vphonewin/tools/inject_static_tc.sh
echo "=== [4] apply dyld_v6 ==="
grep -q '^apfs ' /proc/modules || insmod /home/ard/kbuild/apfs/apfs.ko
L=$(losetup --show -f -o 1048576 "$IMG"); M=$(mktemp -d)
trap 'umount -q "$M" 2>/dev/null||true; losetup -d "$L" 2>/dev/null||true; rmdir "$M" 2>/dev/null||true' EXIT
mount -t apfs -o readwrite,vol=1 "$L" "$M"
rm -f "$M/usr/lib/dyld"; cp "$W/dyld_v6" "$M/usr/lib/dyld"; chmod 0755 "$M/usr/lib/dyld"; sync
umount "$M"; losetup -d "$L"; rmdir "$M"; trap - EXIT
chown ard:ard "$IMG"
echo "DONE. Boot TC=$TCDIR/merged6.trst.bin"
