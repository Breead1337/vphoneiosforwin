with open('/home/ard/vrwork/us.log', 'r', errors='replace') as f:
    for _ in range(5000):
        line = f.readline()
        if 'Taking exception 2 [SVC]' in line:
            print("Found SVC line:")
            print(line, end='')
            for _ in range(15):
                print(f.readline(), end='')
            break
