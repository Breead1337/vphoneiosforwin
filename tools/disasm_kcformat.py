import capstone
with open('/home/ard/vrwork/kernelcache.release.raw.bin', 'rb') as f:
    kc = f.read()
md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)
base = 0xfffffe0007004000

# Walk backwards from `bl panic` @0x9271320 to find function prolog (pacibsp).
va_start = 0xfffffe00092710e8
va_end   = 0xfffffe00092711f0
fo = va_start - base
for insn in md.disasm(kc[fo:fo+(va_end-va_start)], va_start):
    marker = ""
    if insn.address == 0xfffffe0009271320:
        marker = " <-- bl panic Invalid KC Kind"
    print(f"0x{insn.address:x}: {insn.mnemonic:8s} {insn.op_str}{marker}")
