#!/bin/bash
C=/home/ard/vrwork/boot_c1b.console
SL=/home/ard/vrwork/svc.log
echo "=== graft/ignition context ==="
grep -anE 'graft|cryptex|ignite|ignition|not present|already available|not grafted|continuing|object|commit|select-boot|mount-phase' "$C" | sed -n '1,45p' | cut -c1-170
echo
echo -n "ignite() returned lines: "; grep -ac 'ignite() returned' "$C"
echo -n "hello from launchd: "; grep -ac 'hello from launchd' "$C"
echo -n "process starts (.01): "; grep -ac 'dyld_shared_cache_arm64e\.01"' "$SL"
echo "=== executables spawned ==="
grep -aoE '"/(sbin|usr/sbin|usr/libexec|System/Library/CoreServices|bin|usr/bin)/[A-Za-z0-9_./-]+"' "$SL" | sort -u | head -40
