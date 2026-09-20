import re

with open('/home/ard/vrwork/us.log', 'r', errors='replace') as f:
    lines = f.readlines()

svc_blocks = []
cur_block = []
in_svc = False

for line in lines[-20000:]:
    if 'Taking exception 2 [SVC]' in line:
        if cur_block:
            svc_blocks.append(cur_block)
        cur_block = [line.strip()]
        in_svc = True
    elif in_svc:
        if line.startswith('Taking exception') or line.startswith('Exception return'):
            cur_block.append(line.strip())
            if line.startswith('Exception return from AArch64 EL1 to AArch64 EL0'):
                svc_blocks.append(cur_block)
                cur_block = []
                in_svc = False
        else:
            cur_block.append(line.strip())

print(f"Captured {len(svc_blocks)} recent SVC calls.")
for i, b in enumerate(svc_blocks[-15:]):
    print(f"\n--- SVC #{len(svc_blocks)-15+i} ---")
    for l in b:
        if any(k in l for k in ['SVC', 'PC', 'ESR', 'SPSR', 'ELR', 'x16', 'x0', 'x1']):
            print(" ", l)
