import capstone
with open('/home/ard/vrwork/kernelcache.release.raw.bin', 'rb') as f:
    kc = f.read()
md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)
base = 0xfffffe0007004000

for tgt in [0xfffffe00089fd444, 0xfffffe000924d2e8]:
    print(f"\n=== func @ 0x{tgt:x} ===")
    fo = tgt - base
    for insn in md.disasm(kc[fo:fo+0x100], tgt):
        print(f"0x{insn.address:x}: {insn.mnemonic:8s} {insn.op_str}")
