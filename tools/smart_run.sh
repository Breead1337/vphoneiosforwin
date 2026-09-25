#!/bin/bash
# Retry boot until one reaches Data mount; capture the far=0xe00 detailed dump.
W=/home/ard/vrwork
export DISPLAY=:0 VR_EXCLOG=1 VR_SVCLOG=1
export ROOT2=$W/root2.big.img TC=/mnt/d/vphonewin/_work/tc/merged7.trst.bin
for att in 1 2 3 4 5 6; do
  echo "=== ATTEMPT $att ==="
  killall -9 qemu-system-aarch64 2>/dev/null; sleep 2
  rm -f $W/exc.log $W/boot_sr.console
  T=1600 bash /mnt/d/vphonewin/tools/boot_big.sh > $W/boot_sr.console 2>&1 &
  BPID=$!
  good=0
  for k in $(seq 1 160); do
    sleep 10
    if grep -aq 'mounting volume Data' $W/boot_sr.console 2>/dev/null; then good=1; echo "  reached Data mount at ~${k}0s"; break; fi
    if grep -aq 'far=0x4000' $W/exc.log 2>/dev/null; then echo "  early PPL crash (far=0x4000) at ~${k}0s -> retry"; break; fi
    if ! kill -0 $BPID 2>/dev/null; then echo "  boot proc exited early -> retry"; break; fi
  done
  if [ $good = 1 ]; then
    # wait for the far=0xe00 crash + detailed dump
    for k in $(seq 1 30); do
      sleep 6
      if grep -aq 'far=0xe00' $W/exc.log 2>/dev/null; then echo "  GOT far=0xe00"; break; fi
      if grep -aq 'Corefile is not yet' $W/boot_sr.console 2>/dev/null; then sleep 4; break; fi
    done
    echo "=== DATA-MOUNT CRASH DETAILED DUMP ==="
    grep -aA10 'far=0xe00' $W/exc.log 2>/dev/null | head -14
    echo "=== boot tasks reached ==="; grep -aoE '\([a-z0-9-]+\) <Notice>: Doing boot task' $W/boot_sr.console | sort -u | tail
    killall -9 qemu-system-aarch64 2>/dev/null
    exit 0
  fi
  killall -9 qemu-system-aarch64 2>/dev/null; sleep 1
done
echo "=== all attempts stalled/crashed early ==="
grep -aA10 'far=0x4000' $W/exc.log 2>/dev/null | head -14
killall -9 qemu-system-aarch64 2>/dev/null
