import re

# XNU syscall numbers (BSD)
bsd_syscalls = {
    1: "exit", 2: "fork", 3: "read", 4: "write", 5: "open", 6: "close", 7: "wait4",
    9: "link", 10: "unlink", 12: "chdir", 13: "fchdir", 14: "mknod", 15: "chmod",
    16: "chown", 20: "getpid", 23: "setuid", 24: "getuid", 25: "geteuid", 33: "access",
    37: "kill", 39: "getppid", 42: "pipe", 43: "getegid", 44: "profil", 46: "sigaction",
    47: "sigprocmask", 48: "getlogin", 53: "sigaltstack", 54: "ioctl", 56: "revoke",
    58: "readlink", 59: "execve", 60: "umask", 73: "munmap", 74: "mprotect", 75: "madvise",
    80: "getgroups", 81: "setgroups", 89: "getdtablesize", 90: "dup2", 92: "fcntl",
    93: "select", 97: "socket", 98: "connect", 116: "gettimeofday", 121: "writev",
    128: "rename", 133: "sendto", 136: "mkdir", 137: "rmdir", 138: "utimes", 147: "setsockopt",
    151: "readv", 180: "pwrite", 194: "getrlimit", 195: "setrlimit", 198: "mmap",
    202: "sysctl", 204: "undelete", 216: "stat64", 217: "fstat64", 218: "lstat64",
    220: "getattrlist", 221: "setattrlist", 225: "getdirentries64", 234: "statfs64",
    235: "fstatfs64", 236: "fsgetpath", 286: "pthread_sigmask", 327: "issetugid",
    329: "pthread_kill", 336: "proc_info", 338: "stat64_extended", 339: "lstat64_extended",
    340: "fstat64_extended", 344: "getdirentriesattr", 357: "getaudit_addr",
    362: "kqueue", 363: "kevent", 366: "fsctl", 372: "workq_open", 373: "workq_kernreturn",
    380: "kevent64", 397: "open_nocancel", 398: "close_nocancel", 399: "read_nocancel",
    400: "write_nocancel", 401: "openbyid_nocancel", 423: "openat", 424: "openat_nocancel",
    438: "fstatat64", 443: "proc_trace_log", 444: "bsdthread_ctl", 446: "csrctl",
    447: "guarded_open_np", 448: "guarded_close_np", 449: "guarded_kqueue_np",
    462: "memorystatus_control", 471: "os_fault", 472: "os_alloc_once",
    515: "coalition", 516: "coalition_info", 522: "proc_info_extended_id"
}

# Mach trap numbers (negative in XNU convention)
mach_traps = {
    -10: "kernelrpc_mach_vm_allocate_trap",
    -12: "kernelrpc_mach_vm_deallocate_trap",
    -14: "kernelrpc_mach_vm_protect_trap",
    -15: "kernelrpc_mach_vm_map_trap",
    -16: "kernelrpc_mach_port_allocate_trap",
    -18: "kernelrpc_mach_port_deallocate_trap",
    -19: "kernelrpc_mach_port_mod_refs_trap",
    -21: "kernelrpc_mach_port_insert_right_trap",
    -24: "mach_reply_port",
    -25: "thread_self_trap",
    -26: "task_self_trap",
    -27: "host_self_trap",
    -31: "mach_msg_trap",
    -32: "mach_msg_overwrite_trap",
    -33: "semaphore_signal_trap",
    -34: "semaphore_signal_all_trap",
    -35: "semaphore_wait_trap",
    -36: "semaphore_wait_signal_trap",
    -37: "semaphore_timedwait_trap",
    -38: "semaphore_timedwait_signal_trap",
    -89: "mach_timebase_info_trap",
    -90: "mach_wait_until_trap",
    -91: "mk_timer_create_trap",
    -92: "mk_timer_destroy_trap",
    -93: "mk_timer_arm_trap",
    -94: "mk_timer_cancel_trap"
}

print("Scanning us.log for SVC executions and register dumps...")
with open('/home/ard/vrwork/us.log', 'r', errors='replace') as f:
    lines = f.readlines()

svc_count = 0
unique_svcs = set()
recent_calls = []

for i, line in enumerate(lines):
    if 'Taking exception 2 [SVC]' in line:
        svc_count += 1
        # look ahead up to 15 lines for ESR, ELR, x16
        block = lines[i:min(i+15, len(lines))]
        esr = ""
        elr = ""
        for b in block:
            if '...with ESR' in b:
                esr = b.strip()
            if '...with ELR_GL' in b or '...with ELR' in b:
                elr = b.strip()
        recent_calls.append((svc_count, esr, elr))

print(f"Total SVCs found: {svc_count}")
print(f"First 20 SVCs:")
for num, esr, elr in recent_calls[:20]:
    print(f"  #{num}: {esr} | {elr}")

print(f"\nLast 30 SVCs:")
for num, esr, elr in recent_calls[-30:]:
    print(f"  #{num}: {esr} | {elr}")
