import capstone
with open('/home/ard/vrwork/kernelcache.release.raw.bin', 'rb') as f:
    kc = f.read()

md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)
base = 0xfffffe0007004000

# Candidate 1: slide = 0x412a7890 (from cstring), static PC = 0x8a08dbc
# Candidate 2: slide = 0x412a0000 (from prev assumption), static PC = 0x8ab064c
# Show both windows.
for label, pc in [("cstring-slide 0x412a7890", 0xfffffe0008a08dbc),
                  ("aligned-slide 0x412a0000", 0xfffffe0008ab064c)]:
    print(f"=== {label} PC=0x{pc:x} ===")
    fo = pc - base - 0x30
    for insn in md.disasm(kc[fo:fo + 0x80], pc - 0x30):
        m = " <-- UDEF PC" if insn.address == pc else ""
        print(f"0x{insn.address:x}: {insn.mnemonic:8s} {insn.op_str}{m}")
    print()
