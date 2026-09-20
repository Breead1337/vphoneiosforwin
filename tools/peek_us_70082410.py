with open('/home/ard/vrwork/us.log', 'r', errors='ignore') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '0x70082410' in line:
        start = max(0, i - 10)
        end = min(len(lines), i + 15)
        print("".join(lines[start:end]))
        break
