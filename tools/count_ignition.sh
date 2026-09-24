#!/bin/bash
C=/home/ard/vrwork/boot_t900.console
echo "file lines: $(wc -l < "$C")"
echo -n "Darwin Ignition Sequence: "; grep -ac 'Darwin Ignition Sequence' "$C"
echo -n "hello from launchd: "; grep -ac 'hello from launchd' "$C"
echo -n "ignite() returned: "; grep -ac 'ignite() returned' "$C"
echo -n "ignition boot failed: "; grep -ac 'ignition boot failed' "$C"
echo -n "mounting preboot: "; grep -ac 'mounting preboot' "$C"
echo "=== last 25 console lines ==="
tail -25 "$C" | cut -c1-160
