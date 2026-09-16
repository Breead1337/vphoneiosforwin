import capstone

f = r"D:\vphonewin\fw\cloud\raw\LLB.vresearch101.RELEASE.bin"
d = open(f, "rb").read()
base = 0x7006c000
md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)

for i in md.disasm(d, base):
    if i.mnemonic in ("msr", "mrs"):
        op = i.op_str.lower()
        if any(x in op for x in ("ttbr", "tcr", "sctlr", "vbar", "mair")):
            print(f"{hex(i.address)}: {i.mnemonic} {i.op_str}")
