#!/bin/bash
C=/home/ard/vrwork/boot_resign.console
SL=/home/ard/vrwork/svc.log
echo "=== ignition/graft/stage context ==="
grep -anE 'graft|cryptex|ignite|ignition|commit-boot|select-boot|mount-phase|detect-installed|restore-datapartition|rem-enable|not present|already available|not grafted|committed|Corefile' "$C" | sed -n '1,50p' | cut -c1-165
echo
echo -n "hello from launchd: "; grep -ac 'hello from launchd' "$C"
echo -n "ignite() returned: "; grep -aoE 'ignite\(\) returned [0-9]+' "$C" | sort | uniq -c
echo -n "failed to open os cryptex: "; grep -ac 'failed to open os cryptex' "$C"
echo -n "process starts (.01): "; grep -ac 'dyld_shared_cache_arm64e\.01"' "$SL"
echo "=== executables spawned ==="
grep -aoE '"/(sbin|usr/sbin|usr/libexec|System/Library/CoreServices|System/Library/Frameworks|bin|usr/bin)/[A-Za-z0-9_./-]+"' "$SL" | sort -u | head -50
echo "=== svc.log size ==="; wc -l "$SL"
