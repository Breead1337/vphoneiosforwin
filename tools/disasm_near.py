import struct, capstone

kc = open('fw/cloud/raw/kernelcache.research.vresearch101.bin', 'rb')
# Let's inspect 0xb0000 to 0xb5000 in kernelcache
kc.seek(730260 - 0x1000)
code = kc.read(0x2000)
md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)

# Find functions around this area
va_base = 0xfffffe0007008000 + (730260 - 0x1000 - 0x4000)
print(f"Disassembling around {va_base:#x}:")
for ins in md.disasm(code[:0x800], va_base):
    if ins.mnemonic in ['ret', 'retab', 'pacibsp', 'bti']:
        print(f"  {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")
