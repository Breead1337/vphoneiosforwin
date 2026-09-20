import struct
import capstone

kc_path = "/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin"

with open(kc_path, "rb") as f:
    data = f.read()

text_exec_va = 0xfffffe0007a94000
text_exec_off = 0x00a90000

# Search all branches in vnode_check_signature (0xfffffe0007d56dd4 to 0xfffffe0007d58600)
# that jump into the range 0xfffffe0007d58448..0xfffffe0007d584cc
start_va = 0xfffffe0007d56dd4
end_va   = 0xfffffe0007d58600

start_off = text_exec_off + (start_va - text_exec_va)
end_off   = text_exec_off + (end_va - text_exec_va)

md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)
md.detail = True

target_range = range(0xfffffe0007d58440, 0xfffffe0007d584d0, 4)

for insn in md.disasm(data[start_off:end_off], start_va):
    for op in insn.operands:
        if op.type == capstone.arm64.ARM64_OP_IMM:
            if op.imm in target_range:
                print(f"Branch at 0x{insn.address:x}: {insn.mnemonic:8s} {insn.op_str} -> targets 0x{op.imm:x}")

