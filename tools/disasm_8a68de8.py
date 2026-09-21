import capstone
with open('/home/ard/vrwork/kernelcache.release.raw.bin', 'rb') as f:
    kc = f.read()
md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)
base = 0xfffffe0007004000

# The KDA happened at static PC 0x8ab05e4 (mov x0, x20; bl 0x8a68de8) with x20=0 (NULL).
# Show target and its prolog.
for tgt in [0xfffffe0008a68de8, 0xfffffe0008ab05dc]:
    print(f"\n=== func at 0x{tgt:x} ===")
    fo = tgt - base
    for insn in md.disasm(kc[fo:fo+0x60], tgt):
        print(f"0x{insn.address:x}: {insn.mnemonic:8s} {insn.op_str}")
