import capstone

md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)

f = open('/home/ard/vrwork/launchd', 'rb')
f.seek(0x3108)
code = f.read(128)
print("Disassembly of launchd at file offset 0x3108:")
for ins in md.disasm(code, 0x103108):
    print(f"  {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")
