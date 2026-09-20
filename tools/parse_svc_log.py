with open("/home/ard/vrwork/svc.log", "r") as f:
    lines = f.readlines()

print(f"Total SVC entries in svc.log: {len(lines)}")

print("\n--- First 30 SVCs ---")
for l in lines[:30]:
    print(l.strip())

print("\n--- All distinct UNIX syscalls ---")
unix_calls = set()
for l in lines:
    if "UNIX" in l:
        parts = l.strip().split("]")
        if len(parts) > 0:
            unix_calls.add(parts[0])
for u in sorted(unix_calls):
    print(u)

print("\n--- Last 50 SVCs ---")
for l in lines[-50:]:
    print(l.strip())
