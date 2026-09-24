#!/bin/bash
python3 /mnt/d/vphonewin/tools/cryptex1_disasm.py > /home/ard/vrwork/cryptex1_disasm.out 2>&1
echo "lines: $(wc -l < /home/ard/vrwork/cryptex1_disasm.out)"
head -120 /home/ard/vrwork/cryptex1_disasm.out
