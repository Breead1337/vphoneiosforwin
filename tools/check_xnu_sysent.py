# Standard BSD syscall numbers in XNU:
# 1 = exit
# 2 = fork
# 3 = read
# 4 = write
# 5 = open
# 6 = close
# 7 = wait4
# ...
# 50 = setlogin
# ...
# 197 = mmap
# Wait, let's check what 197 is in XNU:
# In FreeBSD: 197 is mmap
# In macOS / XNU:
# Let's check kernelcache for syscall table!
import struct

kc = open('/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin', 'rb')
data = kc.read()

# Let's find sysent table in kernelcache!
# sysent struct:
# struct sysent {
#    int16_t sy_narg;
#    int8_t  sy_resv;
#    int8_t  sy_flags;
#    uint32_t sy_call_offset or uint64_t sy_call;
#    uint32_t sy_arg_munge32_offset;
#    uint32_t sy_arg_munge64_offset;
#    int32_t  sy_return_type;
#    uint16_t sy_arg_bytes;
# };
# Or let's search for string "mmap" or "setlogin" or "open" in kernelcache!
pos = 0
for name in [b"setlogin", b"mmap", b"posix_spawn", b"execve", b"kevent"]:
    p = data.find(name + b"\x00")
    print(f"String {name.decode()}: offset={p:#x}")
