import struct
import capstone

kc_path = "/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin"
with open(kc_path, "rb") as f:
    data = f.read()

text_exec_va = 0xfffffe0007a94000
text_exec_off = 0x00a90000
text_exec_sz = 0x0183c000
s_data = data[text_exec_off:text_exec_off + text_exec_sz]

target_va = 0xfffffe0007d53c84

md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)
md.detail = True

print(f"Searching callers of 0x{target_va:x}...")
for i in range(0, len(s_data), 4):
    insn_val = struct.unpack_from("<I", s_data[i:i+4])[0]
    # BL instruction: (insn_val & 0xfc000000) == 0x94000000
    if (insn_val & 0xfc000000) == 0x94000000:
        imm26 = insn_val & 0x3ffffff
        if imm26 & (1 << 25): imm26 -= (1 << 26)
        pc = text_exec_va + i
        target = pc + (imm26 << 2)
        if target == target_va:
            print(f"Caller BL at 0x{pc:x}:")
            dis_start = max(0, i - 16)
            dis_end = min(len(s_data), i + 32)
            for insn in md.disasm(s_data[dis_start:dis_end], text_exec_va + dis_start):
                m = "==> " if insn.address == pc else "    "
                print(f"{m}0x{insn.address:x}: {insn.mnemonic:8s} {insn.op_str}")

