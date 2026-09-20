import sys

with open("/home/ard/vrwork/us.log", "r", errors="ignore") as f:
    for line in f:
        if "vbar" in line.lower() or "slide" in line.lower():
            print(line.strip())
