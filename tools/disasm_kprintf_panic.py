import capstone
with open('/home/ard/vrwork/kernelcache.release.raw.bin', 'rb') as f:
    kc = f.read()

md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)
base = 0xfffffe0007004000

# kprintf-tag gexit-panic elr = 0xfffffe0041059340. Try both kbase candidates:
for label, slide in [("kbase=0x8a5f000", 0x37d84000),
                     ("kbase=0x89fb000", 0x37de8000)]:
    static_pc = 0xfffffe0041059340 - slide
    print(f"\n=== {label}, slide=0x{slide:x} -> static PC = 0x{static_pc:x} ===")
    fo = static_pc - base - 0x40
    if 0 <= fo < len(kc) - 0x180:
        for insn in md.disasm(kc[fo:fo+0x180], static_pc - 0x40):
            m = " <-- gexit ELR" if insn.address == static_pc else ""
            print(f"0x{insn.address:x}: {insn.mnemonic:8s} {insn.op_str}{m}")
    else:
        print("(out of range)")
