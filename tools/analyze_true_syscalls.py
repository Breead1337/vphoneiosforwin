import re
from collections import Counter

c_mach = Counter()
c_bsd = Counter()

# Known Mach traps:
mach_traps = {
    -10: "mach_reply_port",
    -12: "mach_task_self",
    -14: "mach_host_self",
    -26: "mach_msg_trap",
    -27: "mach_msg_overwrite_trap",
    -28: "semaphore_signal_trap",
    -29: "semaphore_signal_all_trap",
    -30: "semaphore_signal_thread_trap",
    -31: "semaphore_wait_trap",
    -32: "semaphore_wait_signal_trap",
    -33: "semaphore_timedwait_trap",
    -36: "task_for_pid",
    -89: "mach_timebase_info_trap",
    -90: "mach_wait_until_trap",
    -91: "mk_timer_create_trap",
    -92: "mk_timer_destroy_trap",
    -93: "mk_timer_arm_trap",
    -94: "mk_timer_cancel_trap",
    -95: "mk_timer_arm_leeway_trap"
}

# Known BSD syscalls:
bsd_syscalls = {
    1: "exit", 2: "fork", 3: "read", 4: "write", 5: "open", 6: "close", 7: "wait4",
    9: "link", 10: "unlink", 12: "chdir", 13: "fchdir", 14: "mknod", 15: "chmod",
    16: "chown", 20: "getpid", 23: "setuid", 24: "getuid", 25: "geteuid",
    33: "access", 37: "kill", 39: "getppid", 48: "sigaction", 50: "setlogin",
    58: "readlink", 59: "execve", 73: "munmap", 74: "mprotect", 75: "msync",
    97: "socket", 98: "connect", 101: "bind", 104: "bind", 116: "gettimeofday",
    194: "munmap", 195: "mprotect", 196: "msync", 197: "mmap",
    202: "sysctl", 294: "shared_region_check_np", 295: "shared_region_map_and_slide_np",
    327: "issetugid", 340: "shared_region_map_np",
    363: "kevent64", 366: "bsdthread_register", 367: "workq_open", 368: "workq_kernreturn",
    397: "openat", 421: "proc_info", 443: "csrctl", 515: "ulock_wait", 516: "ulock_wake"
}

with open('/home/ard/vrwork/svc.log', 'r', errors='ignore') as f:
    for line in f:
        m = re.search(r'x16=0x([0-9a-fA-F]+)', line)
        if m:
            x16 = int(m.group(1), 16)
            # convert to 32-bit signed
            if x16 >= 0x8000000000000000:
                x16_s = x16 - 0x10000000000000000
            elif x16 >= 0x80000000:
                x16_s = x16 - 0x100000000
            else:
                x16_s = x16

            if x16_s < 0:
                name = mach_traps.get(x16_s, f"mach_trap_{x16_s}")
                c_mach[name] += 1
            else:
                name = bsd_syscalls.get(x16_s, f"bsd_syscall_{x16_s}")
                c_bsd[name] += 1

print("=== MACH TRAPS from x16 ===")
for name, cnt in c_mach.most_common(20):
    print(f"  {name:30s}: {cnt}")

print("\n=== BSD SYSCALLS from x16 ===")
for name, cnt in c_bsd.most_common(20):
    print(f"  {name:30s}: {cnt}")
