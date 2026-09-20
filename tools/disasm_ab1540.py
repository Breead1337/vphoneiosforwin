import struct
import capstone

kc_path = "/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin"
with open(kc_path, "rb") as f:
    data = f.read()

text_exec_va = 0xfffffe0007a94000
text_exec_off = 0x00a90000
md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)

start_va = 0xfffffe0008ab1500
end_va = 0xfffffe0008ab1600
off = text_exec_off + (start_va - text_exec_va)
sz = end_va - start_va

for insn in md.disasm(data[off:off+sz], start_va):
    print(f"0x{insn.address:x}: {insn.mnemonic:8s} {insn.op_str}")
