import capstone

with open('/home/ard/vrwork/kernelcache.release.raw.bin', 'rb') as f:
    kc = f.read()

md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)
base = 0xfffffe0007004000

# Look wide back to find function prolog (pacibsp / stp x29,x30) for _captureiBICKCV
# panic PC = 0xfffffe0008ab064c, LR back to caller = 0xfffffe0008aafc9c (in another func)
va_start = 0xfffffe0008ab0000
va_end   = 0xfffffe0008ab0700
foff = va_start - base
for insn in md.disasm(kc[foff:foff + (va_end - va_start)], va_start):
    marker = " <-- PANIC" if insn.address == 0xfffffe0008ab064c else ""
    print(f"0x{insn.address:x}: {insn.mnemonic:8s} {insn.op_str}{marker}")

print("\n=== Caller site @ static LR 0xfffffe0008aafc9c ===")
va2 = 0xfffffe0008aafc40
foff2 = va2 - base
for insn in md.disasm(kc[foff2:foff2 + 0x100], va2):
    marker = " <-- return addr" if insn.address == 0xfffffe0008aafc9c else ""
    print(f"0x{insn.address:x}: {insn.mnemonic:8s} {insn.op_str}{marker}")
