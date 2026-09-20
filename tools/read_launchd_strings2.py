with open('/home/ard/vrwork/launchd', 'rb') as f:
    data = f.read()

def read_str(addr):
    off = addr - 0x100000000
    end = data.find(b'\x00', off)
    return data[off:end].decode('latin1', errors='replace')

addrs = [
    0x1000623be, 0x10005f90c, 0x1000622dd, 0x1000622eb, 0x1000622fa,
    0x10006231d, 0x10006233b, 0x10005f83e, 0x10005bed6, 0x10005a750
]
for a in addrs:
    print(f'{hex(a)}: "{read_str(a)}"')
