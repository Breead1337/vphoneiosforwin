#!/bin/bash
KC=/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin
echo "=== gigalocker strings in research KC ==="
grep -aboE 'gigalocker' "$KC" | head
echo "--- init_data_protection ---"
grep -aboE 'init_data_protection' "$KC" | head
echo "--- xarts ---"
grep -aboE '/private/xarts' "$KC" | head
echo "=== 3rd spawn full arg (data-protection binary) ==="
grep -aE '\(posix_spawn\)' /home/ard/vrwork/svc.log | tail -1 | grep -aoE 's1="[^"]*"'
echo "=== data-protection context in console (5 lines before gigalocker) ==="
grep -aB6 'Gigalocker file' /home/ard/vrwork/boot_sprr.console | grep -avE '^\[SVC' | tail -8
