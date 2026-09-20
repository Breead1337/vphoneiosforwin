with open("/home/ard/vrwork/us.log", "r", errors="ignore") as f:
    el0_lines = []
    for line in f:
        if "to AArch64 EL0" in line or "from AArch64 EL0" in line or "Taking exception" in line and "EL0" in line:
            el0_lines.append(line.strip())
            if len(el0_lines) > 500:
                break

print(f"Total EL0 transitions logged (first 500): {len(el0_lines)}")
for l in el0_lines[:50]:
    print(l)
if len(el0_lines) > 50:
    print("...")
    for l in el0_lines[-30:]:
        print(l)
