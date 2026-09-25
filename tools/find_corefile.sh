#!/bin/bash
KC=/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin
echo "=== corefile-related strings ==="
grep -aboE "Corefile is not yet initialized|Cannot write a coredump|Current Magic|is not yet initialized" "$KC" | head
echo "=== 'coredump'/'corefile'/'kern_dump' symbol strings ==="
grep -aboE "kern_dump|coredump|corefile|dump_savearea|kdp_core|core_dump|proc_core" "$KC" | head -20
