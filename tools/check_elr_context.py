with open("/home/ard/vrwork/us.log", "r", errors="ignore") as f:
    prev_lines = []
    for line in f:
        if "with ELR 0x700e0" in line:
            print("=== Exception leading to ELR 0x700e0 ===")
            for p in prev_lines[-10:]:
                print(p.strip())
            print(line.strip())
            break
        prev_lines.append(line)
        if len(prev_lines) > 20:
            prev_lines.pop(0)
