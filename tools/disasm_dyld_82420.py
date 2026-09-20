import capstone

md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)

f = open('/mnt/d/vphonewin/fw/cloud/raw/dyld.bin', 'rb')
f.seek(0x82420)
code = f.read(128)
print("Disassembly of dyld 0x70082420:")
for ins in md.disasm(code, 0x70082420):
    print(f"  {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")
    if ins.mnemonic in ('ret', 'retab'):
        break
