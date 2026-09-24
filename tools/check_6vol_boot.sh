#!/bin/bash
C=/home/ard/vrwork/boot_6vol.console
SL=/home/ard/vrwork/svc.log
echo "=== ignition status in console ==="
echo -n "mounting preboot: "; grep -ac 'mounting preboot' "$C"
echo -n "failed to get volume for role: "; grep -ac 'failed to get volume for role' "$C"
echo -n "ignition boot failed: "; grep -ac 'ignition boot failed' "$C"
echo -n "ignite() returned: "; grep -ac 'ignite() returned' "$C"
echo -n "hello from launchd: "; grep -ac 'hello from launchd' "$C"
echo "--- any preboot success / graft / cryptex lines ---"
grep -aE 'preboot mount point|graft|cryptex|preboot:|committed|select-boot|restore-datapartition|mount-phase' "$C" | head -20 | cut -c1-160
echo
echo "=== process starts (distinct cache .01 opens = processes that mapped cache) ==="
grep -ac 'dyld_shared_cache_arm64e\.01"' "$SL"
echo "=== launchd file opens (plists / LaunchDaemons / real paths) ==="
grep -aoE 's0="/[A-Za-z0-9_./-]{3,}"' "$SL" | sort -u | grep -avE 'dyld' | head -40
echo "=== posix_spawn / execve markers ==="
grep -acE 'posix_spawn|\(execve\)|LaunchDaemon|\.plist' "$SL"
echo "=== last 6 console lines ==="
tail -6 "$C" | cut -c1-160
