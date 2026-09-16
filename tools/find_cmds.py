import re

d = open(r"D:\vphonewin\fw\cloud\raw\LLB.vresearch101.RELEASE.bin", "rb").read()

# iBoot commands usually have a struct with: name_ptr, func_ptr, help_ptr
# Let's search for common iBoot commands: help, nvram, bdev, go, fsboot, bootx, image, bgcolor, etc.
cmds = ["help", "nvram", "bdev", "go", "fsboot", "bootx", "image", "bgcolor", "reboot", "poweroff", "reset", "md", "mw", "setenv", "printenv", "saveenv", "mmu", "ticket", "resume"]

found = []
for c in cmds:
    cb = c.encode() + b'\x00'
    pos = d.find(cb)
    if pos != -1:
        found.append((c, hex(pos)))

print("Found commands:", found)

# Let's search for all lowercase alphanumeric strings between 2 and 16 chars followed by null, in the string table area
print("Scanning strings in rodata...")
# Look for help text strings
matches = re.findall(rb'[a-z][a-z0-9_\-]{2,15}\x00', d)
common_cmds = set([m[:-1].decode() for m in matches])
print(f"Total potential strings: {len(common_cmds)}")
known = [c for c in common_cmds if c in ["help", "fsboot", "bdev", "nvram", "bgcolor", "reboot", "reset", "boot", "mmu", "setenv", "saveenv", "getenv", "printenv", "heap", "dump", "mem"]]
print("Interesting matching commands:", known)
