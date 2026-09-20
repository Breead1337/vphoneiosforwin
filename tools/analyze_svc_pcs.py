with open("/home/ard/vrwork/svc.log") as f:
    lines = [l.strip() for l in f]

print("First 20 unique PCs and their SVC entries:")
seen_pc = set()
for l in lines:
    parts = l.split()
    if len(parts) >= 3:
        pc = parts[2]
        if pc not in seen_pc:
            seen_pc.add(pc)
            print(l)
            if len(seen_pc) >= 30:
                break

print("\nHistogram of sysno:")
from collections import Counter
c = Counter()
for l in lines:
    parts = l.split()
    if len(parts) >= 2:
        c[parts[1]] += 1

for sysno, count in c.most_common(25):
    print(f"  {sysno:15s}: {count}")
