import struct
import capstone

kc_path = "/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin"
with open(kc_path, "rb") as f:
    data = f.read()

text_exec_va = 0xfffffe0007a94000
text_exec_off = 0x00a90000

start_va = 0xfffffe0007d6fc80
end_va   = 0xfffffe0007d6fd40

start_off = text_exec_off + (start_va - text_exec_va)
end_off   = text_exec_off + (end_va - text_exec_va)

md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)

for insn in md.disasm(data[start_off:end_off], start_va):
    print(f"0x{insn.address:x}: {insn.mnemonic:10s} {insn.op_str}")
