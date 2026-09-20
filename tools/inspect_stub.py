import capstone

with open('/home/ard/vrwork/aux.test', 'rb') as f:
    f.seek(0x1d6c0)
    chunk = f.read(180)

cs = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)
for i in range(0, len(chunk), 4):
    b = chunk[i:i+4]
    dis = list(cs.disasm(b, 0x1d6c0 + i))
    if dis:
        print(f"0x{dis[0].address:x}: {dis[0].mnemonic} {dis[0].op_str}")
    else:
        val = int.from_bytes(b, 'little')
        print(f"0x{0x1d6c0+i:x}: .word 0x{val:08x}")
