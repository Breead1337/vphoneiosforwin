#!/bin/bash
# Read-only recon: how does dyld locate the shared cache, and what does the rootfs cryptex layout look like?
D=/home/ard/vrwork/dyld_hybrid
echo "qemu procs: $(ps -C qemu-system-aar --no-headers | wc -l)"
ls -la "$D" 2>/dev/null || echo "NO dyld_hybrid"
echo "=== dyld cache-related strings ==="
strings -n 5 "$D" 2>/dev/null | grep -iE 'dyld_shared_cache|com\.apple\.dyld|Cryptexes|/System/Library/dyld|no dyld cache|shared region|Preboot|cryptex' | sort -u | head -80
echo "=== 'cache' path-like strings ==="
strings -n 5 "$D" 2>/dev/null | grep -E '^/' | grep -iE 'cache|dyld|cryptex' | sort -u | head -40
