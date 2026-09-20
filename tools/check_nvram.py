import os

path = '/home/ard/vrwork/aux.test'
if not os.path.exists(path):
    path = '_work/aux.test'
    if not os.path.exists(path):
        print("aux.test not found")
        exit(1)

with open(path, 'rb') as f:
    f.seek(0xa00000)
    data = f.read(0x80000)
    print('NVRAM non-zero bytes:', sum(1 for b in data if b != 0))
    idx = data.find(b'boot-args')
    print('boot-args index:', idx)
    if idx != -1:
        print('Around boot-args:', data[max(0, idx-32):idx+64])
    # Search for any strings
    import re
    strings = re.findall(b'[\x20-\x7e]{4,}', data)
    print(f'Found {len(strings)} strings in NVRAM:')
    for s in strings[:30]:
        print('  ', s.decode('latin1'))
