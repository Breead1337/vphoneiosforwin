import capstone

md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)

f = open('/mnt/d/vphonewin/fw/cloud/raw/dyld.bin', 'rb')
f.seek(0x82650)
code = f.read(256)
print("Disassembly of dyld 0x70082650 onwards:")
for ins in md.disasm(code, 0x70082650):
    print(f"  {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")
    if ins.mnemonic in ('ret', 'retab'):
        break
