with open('/home/ard/vrwork/us.log', 'r', errors='ignore') as f:
    for i in range(100):
        line = f.readline()
        if not line: break
        print(line.rstrip())
