import re

with open('/home/ard/vrwork/us.log', 'r', errors='replace') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'Taking exception 2 [SVC]' in line:
        for j in range(i, min(i + 20, len(lines))):
            if '...with ESR' in lines[j] and '0x56000005' in lines[j]:
                print(f"Found open() at line {i}:")
                for k in range(i, min(i + 25, len(lines))):
                    print(" ", lines[k], end='')
                break
