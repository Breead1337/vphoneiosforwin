#!/bin/bash
C=/home/ard/vrwork/boot_6vol.console
echo "LINES=$(wc -l < "$C")"
echo "=== head 70 ==="
head -70 "$C" | cut -c1-200
echo "=== grep for apfs/mount/iBoot/panic/error ==="
grep -anE 'apfs|mount|iBoot|panic|[Ee]rror|not valid|Image4|nx_mount|checkpoint|volume|disk1' "$C" | head -40 | cut -c1-180
