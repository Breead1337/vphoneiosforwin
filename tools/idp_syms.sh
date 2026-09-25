#!/bin/bash
B=/home/ard/vrwork/init_data_protection
echo "=== nm symbols (gigalocker/main/init) ==="
nm "$B" 2>/dev/null | grep -iE 'gigalock|main|init_data|_main|xart' | head -30
echo "=== objdump available? which disassembler ==="
which llvm-objdump objdump aarch64-linux-gnu-objdump 2>/dev/null
echo "=== imported symbols (open/stat/IOConnect/mach) ==="
nm -u "$B" 2>/dev/null | grep -iE 'open|stat|IOConnect|IOServiceOpen|io_connect|mach_msg|creat|mkdir' | head -20
