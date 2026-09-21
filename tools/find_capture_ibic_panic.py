import capstone

with open('/home/ard/vrwork/kernelcache.release.raw.bin', 'rb') as f:
    kc = f.read()

base = 0xfffffe0007004000
# String static VA
str_va = 0xfffffe0007237a3a  # "kIOReturnSuccess == result"

# Find every ADRP+ADD pair loading this exact VA. Then look nearby for `bl` to panic.
md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)
md.detail = True

# Scan all 4-byte-aligned insns; slow but ok for 40MB.
# We'll walk the whole kc.
insns = []
foff = 0
va_start = base

# Only decode text; assume TEXT is bulk of file
data = kc

# Better: scan for `adrp x?, #0xfffffe0007237000` (imm=0x7237000 relative). adrp imm = target_page - pc_page.
# Easier: iterate and disasm blocks near function candidates. Full disasm is huge, but 40MB is ok in seconds.
found = []
prev = {}
for i in md.disasm(data, base):
    if i.mnemonic == 'adrp' and len(i.operands) == 2 and i.operands[1].type == capstone.arm64.ARM64_OP_IMM:
        imm = i.operands[1].imm
        if imm == 0xfffffe0007237000:
            prev[i.operands[0].reg] = i.address
    elif i.mnemonic == 'add' and len(i.operands) == 3:
        # e.g. add x0, x0, #0xa3a
        if i.operands[0].reg == i.operands[1].reg and i.operands[1].reg in prev and i.operands[2].type == capstone.arm64.ARM64_OP_IMM:
            if i.operands[2].imm == 0xa3a:
                found.append(i.address)
                # keep prev for other uses too
print("ADRP+ADD to kIOReturnSuccess==result at:", [hex(x) for x in found])
