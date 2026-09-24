#!/bin/bash
SL=/home/ard/vrwork/svc.log
CON=/home/ard/vrwork/boot_t900.console
echo "=== how many process-starts? (count .00/.01 first-subcache opens) ==="
grep -acE 'dyld_shared_cache_arm64e\.01"' "$SL"
echo "=== all 'open' EL0 syscalls with real paths (what launchd touches) ==="
grep -aE '\(open\)|\(openat\)' "$SL" | grep -aoE 's0="[^"]+"|s1="[^"]+"' | sort | uniq -c | sort -rn | grep -avE 'dyld_v1' | head -40
echo "=== execve/posix_spawn/fork markers ==="
grep -anE '\(fork\)|\(execve\)|posix_spawn|\(wait4\)|/sbin/launchd|/usr/lib/dyld|LaunchDaemon|\.plist' "$SL" | head -30 | cut -c1-150
echo "=== console (kprintf) tail 40 ==="
tail -40 "$CON" 2>/dev/null | cut -c1-200
