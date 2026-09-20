import re
from collections import Counter

# Let's inspect the PC for each imm in us.log
imm_pcs = {}
with open('/home/ard/vrwork/us.log', 'r', errors='ignore') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    m = re.search(r'with ESR 0x15/0x([0-9a-fA-F]+)', line)
    if m:
        esr = int(m.group(1), 16)
        imm = esr & 0xffff
        # search next few lines for ELR or PC
        elr = None
        for j in range(i, min(i + 5, len(lines))):
            m2 = re.search(r'with ELR 0x([0-9a-fA-F]+)', lines[j])
            if m2:
                elr = int(m2.group(1), 16)
                break
        if elr:
            if imm not in imm_pcs:
                imm_pcs[imm] = Counter()
            imm_pcs[imm][elr] += 1

print("Sample imm -> ELR (PC):")
for imm in sorted(imm_pcs.keys()):
    top_elrs = imm_pcs[imm].most_common(3)
    s = ", ".join([f"{elr:#x} ({cnt})" for elr, cnt in top_elrs])
    print(f"  imm=0x{imm:04x} ({imm:3d}): {s}")
