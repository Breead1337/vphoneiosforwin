import struct, capstone

with open('/home/ard/vrwork/launchd', 'rb') as f:
    f.seek(0x18438)
    code = f.read(512)

md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)
print('Disassembly of launchd main() from 0x100018438:')
for ins in md.disasm(code, 0x100018438):
    print(f'  0x{ins.address:08x}: {ins.mnemonic:8s} {ins.op_str}')
