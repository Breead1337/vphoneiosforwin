#!/bin/bash
C=/home/ard/vrwork/boot_restore.console
SL=/home/ard/vrwork/svc.log
echo -n "hello from launchd: "; grep -ac 'hello from launchd' "$C"
echo -n "cryptex1 sniff: "; grep -ac 'cryptex1 sniff' "$C"
echo -n "graft os canonical/os-cryptex fail: "; grep -acE 'failed to open canonical root|failed to open os cryptex' "$C"
echo -n "cryptex1 in svc.log: "; grep -ac 'cryptex1' "$SL"
echo "--- graft context ---"; grep -anE 'graft|cryptex1 sniff|canonical' "$C" | head -12 | cut -c1-150
