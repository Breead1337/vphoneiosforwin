import re
from collections import Counter

def analyze():
    svc_path = "/home/ard/vrwork/svc.log"
    sys_counts = Counter()
    paths = set()
    spawns = []
    
    with open(svc_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            # Extract syscall name
            m = re.search(r'\[SVC(?:-GL)?\s+(\w+)\s+(-?\d+)\s+\(([^)]+)\)\]', line)
            if m:
                sclass, snum, sname = m.groups()
                sys_counts[f"{sclass}:{sname}:{snum}"] += 1
                if "spawn" in sname or "exec" in sname:
                    spawns.append(line.strip())
            
            # Extract strings
            for sm in re.finditer(r's\d="([^"]+)"', line):
                val = sm.group(1)
                if "/" in val or ".plist" in val or "SpringBoard" in val or "backboard" in val:
                    paths.add(val)

    print("=== SYSCALL COUNTS (TOP 25) ===")
    for k, v in sys_counts.most_common(25):
        print(f"{v:6d}  {k}")
        
    print("\n=== SPAWN / EXEC CALLS ===")
    for s in spawns[:20]:
        print(s)
        
    print(f"\n=== PATHS / STRINGS ACCESSED ({len(paths)}) ===")
    for p in sorted(paths):
        print(" ", p)

if __name__ == '__main__':
    analyze()
