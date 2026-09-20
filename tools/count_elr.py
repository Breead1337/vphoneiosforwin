import re
from collections import Counter

elrs = Counter()
with open('/home/ard/vrwork/us.log', 'r', errors='replace') as f:
    for line in f:
        if '...with ELR_GL' in line:
            m = re.search(r'0x[0-9a-fA-F]+', line)
            if m:
                elrs[m.group(0)] += 1

print(f"Total unique ELR_GL: {len(elrs)}")
print("Top 30 ELR_GL:")
for addr, count in elrs.most_common(30):
    print(f"  {addr}: {count}")
