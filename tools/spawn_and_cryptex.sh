#!/bin/bash
C=/home/ard/vrwork/boot_6vol.console
SL=/home/ard/vrwork/svc.log
echo "=== console around cryptex1 sniff (context) ==="
grep -anE 'cryptex1|cryptex|graft|preboot:|ignite|sniff|select-boot|mount-phase|detect-installed|commit-boot' "$C" | head -40 | cut -c1-170
echo
echo "=== what launchd spawned (execve/posix_spawn target paths) ==="
grep -aE '\(execve\)|posix_spawn|244 |\(240 ' "$SL" | grep -aoE 's[0-9]="/[^"]+"' | sort | uniq -c | sort -rn | head -30
echo "=== all distinct executable-looking paths opened ==="
grep -aoE '"/(sbin|usr/sbin|usr/libexec|System/Library/CoreServices|bin|usr/bin)/[A-Za-z0-9_./-]+"' "$SL" | sort -u | head -40
