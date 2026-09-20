import sys
from collections import Counter

def main():
    log_path = sys.argv[1] if len(sys.argv) > 1 else "/home/ard/vrwork/svc.log"
    c = Counter()
    with open(log_path, "r", errors="ignore") as f:
        for line in f:
            if line.startswith("["):
                idx = line.find("]")
                if idx != -1:
                    c[line[:idx+1]] += 1
    
    print("=== Top Syscalls in svc.log ===")
    for tag, count in c.most_common(50):
        print(f"{count:6d}  {tag}")

if __name__ == "__main__":
    main()
