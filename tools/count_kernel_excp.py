from collections import Counter

c = Counter()
with open('/home/ard/vrwork/us.log', 'r', errors='ignore') as f:
    for line_no, line in enumerate(f, 1):
        if line_no >= 342690:
            if 'Taking exception' in line:
                c[line.strip()] += 1

print("Exceptions AFTER line 342690 (Kernel & Userspace):")
for k, v in c.most_common(20):
    print(f"  {k:60s}: {v}")
