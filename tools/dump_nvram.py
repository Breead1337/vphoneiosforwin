with open('/home/ard/vrwork/aux.test', 'rb') as f:
    f.seek(0xa00000)
    data = f.read(0x1000)
pos = 0x30
while pos < len(data) and data[pos] != 0:
    end = data.find(b'\x00', pos)
    print(data[pos:end].decode('latin1'))
    pos = end + 1
