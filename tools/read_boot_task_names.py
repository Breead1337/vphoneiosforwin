with open('/home/ard/vrwork/launchd', 'rb') as f:
    data = f.read()

def read_str(addr):
    off = addr - 0x100000000
    end = data.find(b'\x00', off)
    return data[off:end].decode('latin1', errors='replace')

addrs = [0x10006d976, 0x10006d97b, 0x10006d989, 0x10006d999, 0x100066d59, 0x100066cf8]
for a in addrs:
    print(f'{hex(a)}: "{read_str(a)}"')
