with open('/home/ard/vrwork/launchd', 'rb') as f:
    data = f.read()

pos = 0
while True:
    p = data.find(b'LaunchDaemons', pos)
    if p == -1: break
    start = data.rfind(b'\x00', 0, p) + 1
    end = data.find(b'\x00', p)
    print(f'Found LaunchDaemons at {hex(p)}: {data[start:end].decode("latin1")}')
    pos = p + 1
