import struct, capstone

with open('/mnt/d/vphonewin/fw/cloud/raw/dyld.bin', 'rb') as f:
    f.seek(0xe0700)
    raw = f.read(32)

print("Raw bytes at 0xe0700:")
print(raw.hex())

md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)
for ins in md.disasm(raw, 0x700e0700):
    print(f"  {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")
