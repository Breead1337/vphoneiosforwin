import capstone

md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)

f = open('/home/ard/vrwork/launchd', 'rb')
f.seek(0x5938)
code = f.read(64)
print("Disassembly of launchd at file offset 0x5938:")
for ins in md.disasm(code, 0x105938):
    print(f"  {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")
