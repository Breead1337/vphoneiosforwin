from collections import Counter

c_sysno = Counter()
c_pc = Counter()
with open('/home/ard/vrwork/svc.log') as f:
    for line in f:
        parts = line.split()
        if len(parts) >= 3:
            c_sysno[parts[1]] += 1
            c_pc[parts[2]] += 1

print("Top 30 Sysnos in svc.log:")
for k, v in c_sysno.most_common(30):
    print(f"  {k:20s}: {v}")

print("\nTop 30 PCs in svc.log:")
for k, v in c_pc.most_common(30):
    print(f"  {k:20s}: {v}")
