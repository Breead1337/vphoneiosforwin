#!/bin/bash
# Boot the bigger hybrid image (full dyld cache) and dump logs. Run as user ard (needs ~/inferno, ~/vrwork).
export DISPLAY=:0
cd /home/ard/vrwork || exit 1
killall -9 qemu-system-aarch64 2>/dev/null; sleep 1
cp /home/ard/vrwork/aux.patched2.img /home/ard/vrwork/aux.test
TC=${TC:-/mnt/d/vphonewin/_work/tc/merged2.trst.bin} ROOT2=/home/ard/vrwork/root2.big.img T=${T:-300} bash /mnt/d/vphonewin/tools/run_userspace.sh
