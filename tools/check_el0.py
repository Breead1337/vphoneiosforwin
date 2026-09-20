with open("/home/ard/vrwork/us.log", "r", errors="ignore") as f:
    for line in f:
        if any(k in line for k in ["real_el0", "vr_uslide_auto", "EL0", "Taking exception 0", "Taking exception 1", "Taking exception 2"]):
            print(line.strip()[:150])
            break
    else:
        print("No EL0 matches found")
