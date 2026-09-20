with open('/home/ard/vrwork/us.log', 'r', errors='ignore') as f:
    lines = f.readlines()

idle_count = 0
last_non_idle_idx = -1
for i in range(len(lines) - 1, 342690, -1):
    if 'cbf0' in lines[i]:
        idle_count += 1
    else:
        if last_non_idle_idx == -1 and idle_count > 10:
            last_non_idle_idx = i
            break

print(f"Total idle iterations at end of log: {idle_count}")
print(f"Last non-idle log line: {last_non_idle_idx}")
if last_non_idle_idx != -1:
    start = max(342690, last_non_idle_idx - 40)
    end = min(len(lines), last_non_idle_idx + 10)
    for j in range(start, end):
        print(f"{j:6d}: {lines[j].strip()}")
