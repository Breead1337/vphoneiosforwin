#!/bin/bash
SL=/home/ard/vrwork/svc.log
KP=/home/ard/vrwork/kprintf.log
echo "=== svc.log size ==="; wc -l "$SL" 2>/dev/null
echo "=== cryptex/graft/canonical/launchd in svc.log ==="
grep -aoE 'cryptex1|canonical|graft|/sbin/launchd|current|hello' "$SL" 2>/dev/null | sort | uniq -c | head
echo "=== last 12 EL0 (userspace) svc lines (where it crashed) ==="
grep -aE '^\[SVC    ' "$SL" 2>/dev/null | tail -12 | cut -c1-150
echo "=== kprintf.log: launchd/libignition/cryptex/Corefile ==="
grep -anE 'launchd|libignition|cryptex|Corefile|hello|ignit|dyld' "$KP" 2>/dev/null | head -25 | cut -c1-150
echo "=== kprintf size ==="; wc -l "$KP" 2>/dev/null
