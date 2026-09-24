#!/bin/bash
C=/home/ard/vrwork/boot_v4.console
SL=/home/ard/vrwork/svc.log
echo "=== ignition stage context (graft onward) ==="
grep -anE 'graft|cryptex|ignite|ignition|commit-boot|select-boot|mount-phase|detect-installed|restore-datapartition|rem-enable|optional|continuing|committed|primary ignition|complete' "$C" | sed -n '1,60p' | cut -c1-165
echo
echo -n "hello from launchd: "; grep -ac 'hello from launchd' "$C"
echo "ignite() returned:"; grep -aoE 'ignite\(\) returned [0-9]+' "$C" | sort | uniq -c
echo -n "primary ignition complete: "; grep -ac 'primary ignition complete\|ignition complete\|ignition succeeded' "$C"
echo -n "process starts (.01): "; grep -ac 'dyld_shared_cache_arm64e\.01"' "$SL"
echo "=== executables spawned ==="
grep -aoE '"/(sbin|usr/sbin|usr/libexec|System/Library/CoreServices|System/Library/Frameworks|System/Library/PrivateFrameworks|bin|usr/bin)/[A-Za-z0-9_./-]+"' "$SL" | sort -u | head -60
echo "=== svc.log size ==="; wc -l "$SL"
