#!/bin/bash
# Rebuild root2.big.img as a 6-volume container (matches DeviceTree fstab), then
# re-inject the DSC-augmented StaticTrustCache. qemu must be down. Run as root.
set -e
echo "=== [A] build 6-volume big image (rootfs + full cache; vols 2-5 empty) ==="
SIZEG=28 bash /mnt/d/vphonewin/tools/build_big_hybrid.sh
echo "=== [B] inject DSC StaticTrustCache into new image ==="
bash /mnt/d/vphonewin/tools/apply_dsc_tc.sh
echo "=== [C] verify volume roles in new image ==="
grep -q '^apfs ' /proc/modules || insmod /home/ard/kbuild/apfs/apfs.ko
# read roles straight from the container (offset 1MiB) via role_check on the loop dev backing file:
python3 - <<'PY'
import struct
d=open('/home/ard/vrwork/root2.big.img','rb').read()
for name,exp in {b'Preboot':0x10,b'System':0x1,b'Data':0x40,b'Update':0xc0,b'xART':0x100,b'Hardware':0x140}.items():
    o=d.find(name+b'\x00')
    r=struct.unpack_from('<H',d,o+256+4)[0] if o>=0 else -1
    print(f"{name.decode():9} role=0x{r:x} {'OK' if r==exp else 'BAD'}")
PY
echo "ALL DONE -> root2.big.img (6 volumes)"
