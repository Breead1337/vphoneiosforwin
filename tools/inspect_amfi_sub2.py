import struct
import capstone

kc_path = "/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin"
with open(kc_path, "rb") as f:
    data = f.read()

text_exec_va = 0xfffffe0007a94000
text_exec_off = 0x00a90000

# Print strings around 0xfffffe00071f5000
ro_va = 0xfffffe0007000000
# let's find the file offset of 0xfffffe00071f5000
# In kernelcache Mach-O, let's search for the bytes or calc offset
# We know from find_daemon_port_caller.py that data[0x1f2175] was 0xfffffe00071f6175.
# So va - 0xfffffe0007004000 = file offset?
# Let's check 0xfffffe00071f6175:
# 0xfffffe00071f6175 - 0x1f2175 = 0xfffffe0007004000.
# So file_off = va - 0xfffffe0007004000.
def va2off(va):
    return va - 0xfffffe0007004000

for off_str in [0xa9f, 0xb02, 0xa6d, 0xb2c]:
    va = 0xfffffe00071f5000 + off_str
    fo = va2off(va)
    print(f"String at 0x{va:x}: {repr(data[fo:fo+80].split(b'\\x00')[0])}")

# Let's disassemble from 0xfffffe0007d51f00 to 0xfffffe0007d52120
md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)
start_va = 0xfffffe0007d51ee0
end_va = 0xfffffe0007d52110
fo_code = text_exec_off + (start_va - text_exec_va)
for insn in md.disasm(data[fo_code:fo_code + (end_va - start_va)], start_va):
    print(f"0x{insn.address:x}: {insn.mnemonic:8s} {insn.op_str}")
