import struct
import capstone

kc_path = "/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin"
with open(kc_path, "rb") as f:
    data = f.read()

text_exec_va = 0xfffffe0007a94000
text_exec_off = 0x00a90000
text_exec_sz = 0x0183c000
s_data = data[text_exec_off:text_exec_off + text_exec_sz]

targets = range(0xfffffe0007d57680, 0xfffffe0007d576b8, 4)

md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)

for i in range(0, len(s_data), 4):
    insn_val = struct.unpack_from("<I", s_data[i:i+4])[0]
    # Check unconditional B or conditional B
    pc = text_exec_va + i
    target = None
    if (insn_val & 0xfc000000) == 0x14000000 or (insn_val & 0xfc000000) == 0x94000000:
        imm26 = insn_val & 0x3ffffff
        if imm26 & (1 << 25): imm26 -= (1 << 26)
        target = pc + (imm26 << 2)
    elif (insn_val & 0xff000010) == 0x54000000: # B.cond
        imm19 = (insn_val >> 5) & 0x7ffff
        if imm19 & (1 << 18): imm19 -= (1 << 19)
        target = pc + (imm19 << 2)
    elif (insn_val & 0x7f000000) == 0x35000000 or (insn_val & 0x7f000000) == 0x34000000: # CBZ/CBNZ
        imm19 = (insn_val >> 5) & 0x7ffff
        if imm19 & (1 << 18): imm19 -= (1 << 19)
        target = pc + (imm19 << 2)
    elif (insn_val & 0x7f000000) == 0x36000000 or (insn_val & 0x7f000000) == 0x37000000: # TBZ/TBNZ
        imm14 = (insn_val >> 5) & 0x3fff
        if imm14 & (1 << 13): imm14 -= (1 << 14)
        target = pc + (imm14 << 2)
    
    if target in targets:
        for insn in md.disasm(s_data[i:i+4], pc):
            print(f"Branch at 0x{pc:x} -> 0x{target:x}: {insn.mnemonic} {insn.op_str}")
