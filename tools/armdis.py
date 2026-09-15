# dis.py FILE BASE OFF COUNT  — disassemble raw arm64
import sys, capstone
f, base, off, n = sys.argv[1], int(sys.argv[2],0), int(sys.argv[3],0), int(sys.argv[4])
d = open(f,'rb').read()
md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)
for i in md.disasm(d[off:off+n*4], base+off):
    print(f'{i.address:#x}: {i.bytes.hex()}  {i.mnemonic} {i.op_str}')
