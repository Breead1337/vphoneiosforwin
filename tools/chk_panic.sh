#!/bin/bash
C=/home/ard/vrwork/boot_panic.console
echo "qemu alive: $(ps -C qemu-system-aar --no-headers | wc -l)"
echo "Data mount: $(grep -ac 'mounting volume Data' "$C")"
echo "Corefile:   $(grep -ac 'Corefile' "$C")"
echo "=== panic-ish lines ==="
grep -anaiE 'Original panic|panic\(|panic:|require|assertion|kernel data abort|SPTM' "$C" | tail -20 | cut -c1-170
echo "=== after Data mount (non-SVC) ==="
awk '/mounting volume Data/{f=1} f' "$C" | grep -avE '^\[SVC' | head -20 | cut -c1-160
