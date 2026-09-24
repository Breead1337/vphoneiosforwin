#!/bin/bash
SL=/home/ard/vrwork/svc.log
echo "=== launchd EL0 syscalls from console-open to end (decoded where known) ==="
awk 'NR>=8080 && /^\[SVC    /' "$SL" | cut -c1-150 | \
sed -E 's/x16=0x5 /SYS=open   /; s/x16=0x6 /SYS=close  /; s/x16=0xa /SYS=unlink /; s/x16=0x31 /SYS=getppid/; s/x16=0x49 /SYS=munmap /; s/x16=0x5c /SYS=fcntl? /; s/x16=0x7 /SYS=wait4  /; s/x16=0xca /SYS=sysctl?/; s/x16=0x99 /SYS=mmap?  /; s/x16=0x153 /SYS=t339  /; s/x16=0x1cf /SYS=t463  /' | head -80
echo
echo "=== any strings that look like plist / LaunchDaemons / xpc / config paths anywhere ==="
grep -aoE '"/[A-Za-z0-9_./-]{4,}"' "$SL" | sort -u | grep -avE 'dyld' | head -40
