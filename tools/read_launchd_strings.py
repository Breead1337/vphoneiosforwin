with open('/home/ard/vrwork/launchd', 'rb') as f:
    data = f.read()

def read_str(addr):
    off = addr - 0x100000000
    end = data.find(b'\x00', off)
    return data[off:end].decode('latin1', errors='replace')

for addr in [0x10006221e, 0x100062230, 0x100062247, 0x10006225d, 0x100062279, 0x1000622a0, 0x1000622c5, 0x10006237e]:
    print(f'{hex(addr)}: "{read_str(addr)}"')
