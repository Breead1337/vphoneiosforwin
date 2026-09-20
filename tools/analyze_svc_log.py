with open("/home/ard/vrwork/svc.log") as f:
    lines = f.readlines()
print(f"Total lines in svc.log: {len(lines)}")
print("\nFirst 40 lines:")
for line in lines[:40]:
    print(line.strip())

print("\nLast 40 lines:")
for line in lines[-40:]:
    print(line.strip())

# Check lines with strings
str_lines = [l.strip() for l in lines if 'str=' in l or 's0=' in l or 's1=' in l]
print(f"\nTotal lines with strings: {len(str_lines)}")
for l in str_lines[:50]:
    print(l)
