import struct, capstone

with open('/home/ard/vrwork/launchd', 'rb') as f:
    f.seek(0x49700)
    code = f.read(128)

md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)
print('Disassembly of launchd at 0x100049700:')
for ins in md.disasm(code, 0x100049700):
    print(f'  0x{ins.address:08x}: {ins.mnemonic:8s} {ins.op_str}')
