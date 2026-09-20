from collections import Counter

counts = Counter()
with open('/home/ard/vrwork/us.log', 'r', errors='replace') as f:
    for line in f:
        if '...with ESR 0x15/' in line:
            esr = line.strip().split()[-1]
            counts[esr] += 1

print("Distribution of ESR for SVCs:")
for esr, count in counts.most_common(20):
    print(f"  {esr}: {count}")
