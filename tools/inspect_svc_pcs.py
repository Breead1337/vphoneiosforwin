import sys

def main():
    log_path = sys.argv[1] if len(sys.argv) > 1 else "/home/ard/vrwork/svc.log"
    pcs = {}
    with open(log_path, "r", errors="ignore") as f:
        for line in f:
            if "pc=" in line:
                parts = line.split("pc=")
                pc = parts[1].split()[0]
                pcs[pc] = pcs.get(pc, 0) + 1
    
    print("=== Unique PCs in svc.log ===")
    for pc, count in sorted(pcs.items(), key=lambda x: x[1], reverse=True):
        print(f"{count:6d}  {pc}")

if __name__ == "__main__":
    main()
