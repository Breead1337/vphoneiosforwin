import struct
import capstone

kc_path = "/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin"
with open(kc_path, "rb") as f:
    data = f.read()

text_exec_va = 0xfffffe0007a94000
text_exec_off = 0x00a90000
md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)

# Check string at 0xfffffe00071f8f75
def va2off(va):
    return va - 0xfffffe0007004000

fo = va2off(0xfffffe00071f8f75)
print("String at 0xfffffe00071f8f75:", repr(data[fo:fo+80].split(b'\x00')[0]))

# Disassemble from 0xfffffe0007d57ea0 to 0xfffffe0007d57f20
start_va = 0xfffffe0007d57ea0
end_va = 0xfffffe0007d57f20
off = text_exec_off + (start_va - text_exec_va)
sz = end_va - start_va

for insn in md.disasm(data[off:off+sz], start_va):
    print(f"0x{insn.address:x}: {insn.mnemonic:8s} {insn.op_str}")
