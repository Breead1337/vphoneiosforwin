import struct
import capstone

kc_path = "/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin"
with open(kc_path, "rb") as f:
    data = f.read()

target_page = 0xfffffe00071f6000
target_off = 0x175

# Check string at 0x1f2175
print("Full string:", repr(data[0x1f2175 - 30 : 0x1f2175 + 50]))

# Search in __TEXT_EXEC: vmaddr=0xfffffe0007a94000, fileoff=0x00a90000, size=0x0183c000
text_exec_va = 0xfffffe0007a94000
text_exec_off = 0x00a90000
text_exec_sz = 0x0183c000
s_data = data[text_exec_off:text_exec_off + text_exec_sz]

md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)

for i in range(0, len(s_data) - 8, 4):
    insn_val = struct.unpack_from("<I", s_data[i:i+4])[0]
    if (insn_val & 0x9f000000) == 0x90000000: # ADRP
        immlo = (insn_val >> 29) & 3
        immhi = (insn_val >> 5) & 0x7ffff
        imm = (immhi << 2) | immlo
        if imm & (1 << 20): imm -= (1 << 21)
        pc = text_exec_va + i
        adrp_page = (pc & ~0xfff) + (imm << 12)
        if adrp_page == target_page:
            rd = insn_val & 0x1f
            next_val = struct.unpack_from("<I", s_data[i+4:i+8])[0]
            if (next_val & 0x3fc00000) == 0x11000000: # ADD
                add_imm = (next_val >> 10) & 0xfff
                rn = (next_val >> 5) & 0x1f
                # check if add_imm is close to target_off (sometimes format string starts earlier)
                if rn == rd and abs(add_imm - target_off) < 64:
                    print(f"MATCH at 0x{pc:x} (add_imm=0x{add_imm:x}):")
                    dis_start = max(0, i - 48)
                    dis_end = min(len(s_data), i + 96)
                    for insn in md.disasm(s_data[dis_start:dis_end], text_exec_va + dis_start):
                        m = "==> " if insn.address == pc else "    "
                        print(f"{m}0x{insn.address:x}: {insn.mnemonic:8s} {insn.op_str}")

