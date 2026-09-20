import re

with open('/home/ard/vrwork/us.log', 'r', errors='replace') as f:
    lines = f.readlines()

print(f"Total lines in us.log: {len(lines)}")

# Let's find all ESR values for SVC exceptions
svc_esrs = {}
for i, line in enumerate(lines):
    if 'Taking exception 2 [SVC]' in line:
        # scan next 10 lines for ESR
        for j in range(i, min(i + 15, len(lines))):
            if '...with ESR' in lines[j]:
                m = re.search(r'/0x([0-9a-fA-F]+)', lines[j])
                if m:
                    esr = int(m.group(1), 16)
                    imm = esr & 0xffff
                    svc_esrs[imm] = svc_esrs.get(imm, 0) + 1
                break

print("Unique SVC immediate values (count):")
for imm in sorted(svc_esrs.keys()):
    print(f"  imm = {imm:#06x} ({imm:5d}): count = {svc_esrs[imm]}")
