#!/bin/bash
Q=~/inferno/build/qemu-system-aarch64
W=~/vrwork

# Create a test input script
cat << 'CMDS' > $W/cmds.txt
help
printenv
bdev
CMDS

echo "=== Running QEMU with input commands ==="
(
  sleep 4
  echo "help"
  sleep 1
  echo "printenv"
  sleep 1
) | timeout 10 $Q -M vresearch101 -smp 1 -m 4G -bios /mnt/d/vphonewin/fw/vz/AVPBooter.vresearch1.bin \
  -drive if=pflash,format=raw,file=$W/aux.img -drive if=pflash,format=raw,file=$W/disk.img \
  -display none -serial stdio 2>/dev/null
echo "=== Done ==="
