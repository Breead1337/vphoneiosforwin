#!/bin/bash
D=/home/ard/vrwork/dyld_hybrid
echo "=== capstone? ==="; python3 -c "import capstone; print('capstone', capstone.__version__)" 2>&1 | head -1
echo "=== llvm-objdump? ==="; which llvm-objdump objdump 2>/dev/null
echo "=== cryptex1 sniff related strings ==="
strings -n 5 "$D" | grep -iE 'cryptex1|sniff|canary|not present|not using fallback|ignition failed|already available|graft point' | sort -u | head -40
