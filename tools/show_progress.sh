#!/bin/bash
C=/home/ard/vrwork/${1:-boot_sprr.console}
echo "=== boot tasks ==="
grep -aoE "\([a-z0-9-]+\) <Notice>: Doing boot task" "$C" | sort -u
echo "=== child pids (non-0/1) ==="
grep -aoE "\(pid [0-9]+\)" "$C" | sort -un -t' ' -k2 | uniq | head -30
echo "=== mounts ==="
grep -aoE "mount-complete volume [A-Za-z]+" "$C" | sort -u
echo "=== crash markers ==="
grep -acE "out of range bind|Assertion failed|SIGKILL of init" "$C"
echo "=== last 12 console lines ==="
tail -12 "$C"
