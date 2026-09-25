#!/bin/bash
B=/home/ard/vrwork/init_data_protection
KC=/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin
echo "=== 'doesn'\''t exist' / 'Gigalocker file' in BINARY ==="
grep -aboE "doesn.t exist|Gigalocker file|Failed to initialize gigalocker|gigalocker" "$B" | head
echo "=== same in KERNEL ==="
grep -aboE "doesn.t exist|Gigalocker file|Failed to initialize gigalocker" "$KC" | head
echo "=== binary: is it a fat/thin macho? symbols? ==="
file "$B"
echo "=== all format-ish strings mentioning gigalocker in binary ==="
strings -a "$B" | grep -aiE 'gigalocker' | head
