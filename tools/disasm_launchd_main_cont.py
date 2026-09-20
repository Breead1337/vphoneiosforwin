import struct, capstone

with open('/home/ard/vrwork/launchd', 'rb') as f:
    f.seek(0x1823c)
    code = f.read(512)

md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)
print('Disassembly of launchd main() from 0x10001823c:')
for ins in md.disasm(code, 0x10001823c):
    print(f'  0x{ins.address:08x}: {ins.mnemonic:8s} {ins.op_str}')
