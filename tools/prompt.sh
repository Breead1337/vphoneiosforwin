#!/bin/bash
# boot to iBoot recovery prompt and type commands over UART: bash prompt.sh "help" "printenv" ...
# WAIT = seconds before typing (default 40), T = total timeout
Q=~/inferno/build/qemu-system-aarch64
W=~/vrwork
(
  sleep ${WAIT:-40}
  for c in "$@"; do printf '%s\r' "$c"; sleep ${GAP:-3}; done
) | timeout ${T:-90} $Q -M vresearch101 -smp 1 -m 4G -bios /mnt/d/vphonewin/fw/vz/AVPBooter.vresearch1.bin \
  -drive if=pflash,format=raw,file=$W/aux.img -drive if=pflash,format=raw,file=$W/disk.img \
  -display none -serial stdio $EXTRA 2>/dev/null | sed -n '/Entering recovery/,$p'
