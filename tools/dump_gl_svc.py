import sys

def main():
    log_path = sys.argv[1] if len(sys.argv) > 1 else "/home/ard/vrwork/svc.log"
    with open(log_path, "r", errors="ignore") as f:
        for line in f:
            if "SVC-GL" in line:
                print(line.strip())

if __name__ == "__main__":
    main()
