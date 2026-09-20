with open("/home/ard/vrwork/us.log", "r", errors="ignore") as f:
    matched = 0
    for line in f:
        if "0x700e0" in line:
            print(line.strip())
            matched += 1
            if matched > 30:
                break
