with open('/home/ard/vrwork/us.log', 'r', errors='ignore') as f:
    lines = f.readlines()

first_idle_line = -1
for i in range(len(lines) - 1, 342690, -1):
    if 'cbf0' in lines[i]:
        first_idle_line = i
    else:
        if first_idle_line != -1 and (first_idle_line - i) > 50:
            break

print(f"First idle loop line: {first_idle_line}")
start = max(342690, first_idle_line - 30)
end = min(len(lines), first_idle_line + 15)
for j in range(start, end):
    print(f"{j:6d}: {lines[j].strip()}")
