#!/bin/bash
C=/home/ard/vrwork/boot_c1p.console
SL=/home/ard/vrwork/svc.log
echo "=== ignition/graft/stage context (first pass) ==="
grep -anE 'graft|cryptex|ignite|ignition|commit-boot|select-boot|mount-phase|detect-installed|restore-datapartition|rem-enable|exclave|boot-mode|committed|primary ignition|failed' "$C" | sed -n '1,55p' | cut -c1-165
echo
echo -n "ignite() returned: "; grep -ac 'ignite() returned' "$C"
echo -n "ignition boot failed: "; grep -ac 'ignition boot failed' "$C"
echo -n "hello from launchd: "; grep -ac 'hello from launchd' "$C"
echo -n "process starts (.01): "; grep -ac 'dyld_shared_cache_arm64e\.01"' "$SL"
echo "=== executables spawned (real paths) ==="
grep -aoE '"/(sbin|usr/sbin|usr/libexec|System/Library/CoreServices|System/Library/Frameworks|bin|usr/bin)/[A-Za-z0-9_./-]+"' "$SL" | sort -u | head -50
echo "=== console tail 8 ==="
grep -avE 'Taking exception' "$C" | tail -8 | cut -c1-150
