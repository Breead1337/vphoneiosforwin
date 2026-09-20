with open("/home/ard/vrwork/svc.log", "r") as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
for i, l in enumerate(lines):
    if any(k in l for k in ["s0=", "s1=", "s2="]):
        print(f"[{i}] {l.strip()}")
