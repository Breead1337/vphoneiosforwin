#!/bin/bash
C=/home/ard/vrwork/boot_v6.console
SL=/home/ard/vrwork/svc.log
echo -n "out of range bind: "; grep -ac 'out of range bind' "$C"
echo -n "ignition sequence complete: "; grep -ac 'ignition sequence complete' "$C"
echo -n "entering ondemand: "; grep -ac 'entering ondemand' "$C"
echo -n "Doing boot task: "; grep -ac 'Doing boot task' "$C"
echo -n "process starts (.01 cache opens): "; grep -ac 'dyld_shared_cache_arm64e\.01"' "$SL"
echo -n "Corefile crashes: "; grep -ac 'Corefile is not yet' "$C"
echo "=== boot tasks / spawns / services in console ==="
grep -anE 'Doing boot task|entering ondemand|hello from launchd|posix_spawn|launchctl|com.apple|xpcproxy|backboard|SpringBoard|Assertion|panic' "$C" | tail -30 | cut -c1-155
echo "=== executables spawned (svc) ==="
grep -aoE '"/(sbin|usr/sbin|usr/libexec|System/Library/CoreServices|System/Library/Frameworks|System/Library/PrivateFrameworks|bin|usr/bin)/[A-Za-z0-9_./-]+"' "$SL" | sort -u | head -60
