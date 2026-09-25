#!/bin/bash
C=/home/ard/vrwork/${1:-boot_sprr.console}
echo "qemu alive: $(ps -C qemu-system-aar --no-headers | wc -l)"
echo "boot tasks: $(grep -acE 'Doing boot task' "$C")"
echo "=== after gigalocker (non-SVC lines) ==="
awk '/gigalocker/{f=1} f' "$C" | grep -avE '^\[SVC' | head -50
