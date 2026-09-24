#!/bin/bash
C=/home/ard/vrwork/boot_c1.console
SL=/home/ard/vrwork/svc.log
echo "=== ignition / cryptex1 status ==="
echo -n "cryptex1 sniff: "; grep -ac 'cryptex1 sniff' "$C"
echo -n "detecting cryptex1 directory: "; grep -ac 'detecting cryptex1 directory' "$C"
echo -n "stat cryptex1 canary: "; grep -ac 'stat cryptex1 canary' "$C"
echo -n "ignition failed: "; grep -ac 'ignition failed' "$C"
echo -n "ignite() returned: "; grep -ac 'ignite() returned' "$C"
echo -n "graft: "; grep -ac 'graft' "$C"
echo -n "hello from launchd: "; grep -ac 'hello from launchd' "$C"
echo "--- all libignition lines after cryptex1 (context) ---"
grep -anE 'cryptex|graft|ignite|ignition|sniff|canary|committed|select-boot|mount-phase|detect-installed|restore-datapartition|rem-enable' "$C" | head -50 | cut -c1-160
echo
echo "=== process starts (cache .01 opens) ==="; grep -ac 'dyld_shared_cache_arm64e\.01"' "$SL"
echo "=== executables launchd spawned ==="
grep -aoE '"/(sbin|usr/sbin|usr/libexec|System/Library/CoreServices|bin|usr/bin|System/Library/PrivateFrameworks)/[A-Za-z0-9_./-]+"' "$SL" | sort -u | head -50
echo "=== last 5 console lines ==="; tail -5 "$C" | cut -c1-150
