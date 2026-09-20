import re

with open('/home/ard/vrwork/us.log', 'r', errors='replace') as f:
    lines = f.readlines()

svc_events = []
for i, line in enumerate(lines):
    if 'Taking exception 2 [SVC]' in line:
        block = lines[i:min(i + 15, len(lines))]
        esr = ""
        elr = ""
        for b in block:
            if '...with ESR' in b:
                esr = b.strip()
            if '...with ELR_GL' in b or '...with ELR' in b:
                elr = b.strip()
        svc_events.append((esr, elr))

print(f"Total SVC events: {len(svc_events)}")
print("\nLast 50 SVC events:")
for idx, (esr, elr) in enumerate(svc_events[-50:], len(svc_events) - 50):
    print(f"  #{idx:5d}: {esr} | {elr}")
