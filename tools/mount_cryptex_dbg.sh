#!/bin/bash
DMG=/home/ard/vrwork/cryptex/043-54303-126.dmg
echo "NXSB@0x20:"; od -An -c -j 32 -N 4 "$DMG"
grep -q '^apfs ' /proc/modules || insmod /home/ard/kbuild/apfs/apfs.ko
L=$(losetup --show -f "$DMG")
echo "loop=$L"
M=$(mktemp -d)
echo "--- mount vol=0 ---"; mount -t apfs -o ro,vol=0 "$L" "$M" 2>&1; ls "$M" 2>/dev/null | head; umount "$M" 2>/dev/null
echo "--- mount vol=1 ---"; mount -t apfs -o ro,vol=1 "$L" "$M" 2>&1; ls "$M" 2>/dev/null | head; umount "$M" 2>/dev/null
echo "--- mount no vol ---"; mount -t apfs -o ro "$L" "$M" 2>&1; ls "$M" 2>/dev/null | head; umount "$M" 2>/dev/null
losetup -d "$L"; rmdir "$M"
