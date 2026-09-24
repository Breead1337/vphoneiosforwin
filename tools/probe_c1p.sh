#!/bin/bash
C=/home/ard/vrwork/boot_c1p.console
echo "console lines: $(wc -l < "$C")"
echo "=== grep launchd/dyld/libignition/cryptex/panic/exec/SIGKILL/Corefile/init ==="
grep -anE 'launchd|libignition|cryptex|dyld|panic|exec|SIGKILL|Corefile|initproc|reboot|Assert|abort|not loaded|Library not loaded|hello|ignit' "$C" | head -40 | cut -c1-170
echo "=== lines 250-300 (between the two kernel boots) ==="
sed -n '250,300p' "$C" | cut -c1-150
