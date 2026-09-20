import re

print("Searching us.log for fork, posix_spawn, exec, or other processes...")
with open('/home/ard/vrwork/us.log', 'r', errors='replace') as f:
    for line in f:
        if any(w in line.lower() for w in ['posix_spawn', 'fork', 'execve', 'spawn', 'pid 2', 'pid 3', 'new proc', 'process 1 exec']):
            print("  ", line.strip())
