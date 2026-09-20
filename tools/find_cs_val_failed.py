import struct
import capstone

kc_path = "/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin"
with open(kc_path, "rb") as f:
    data = f.read()

target_str = b"AMFI: code signature validation failed"
pos = 0
str_offsets = []
while True:
    idx = data.find(target_str, pos)
    if idx == -1: break
    str_offsets.append(idx)
    pos = idx + len(target_str)

print("Found string offsets:", [hex(x) for x in str_offsets])

# Find VA of string
# As we saw earlier: va = file_off + 0xfffffe0007004000
text_exec_va = 0xfffffe0007a94000
text_exec_off = 0x00a90000
text_exec_sz = 0x0183c000
s_data = data[text_exec_off:text_exec_off + text_exec_sz]

md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)

for off in str_offsets:
    str_va = off + 0xfffffe0007004000
    print(f"Checking string at VA 0x{str_va:x}...")
    target_page = str_va & ~0xfff
    target_off = str_va & 0xfff
    for i in range(0, len(s_data) - 8, 4):
        insn_val = struct.unpack_from("<I", s_data[i:i+4])[0]
        if (insn_val & 0x9f000000) == 0x90000000:
            immlo = (insn_val >> 29) & 3
            immhi = (insn_val >> 5) & 0x7ffff
            imm = (immhi << 2) | immlo
            if imm & (1 << 20): imm -= (1 << 21)
            pc = text_exec_va + i
            adrp_page = (pc & ~0xfff) + (imm << 12)
            if adrp_page == target_page:
                rd = insn_val & 0x1f
                next_val = struct.unpack_from("<I", s_data[i+4:i+8])[0]
                if (next_val & 0x3fc00000) == 0x11000000:
                    add_imm = (next_val >> 10) & 0xfff
                    rn = (next_val >> 5) & 0x1f
                    if rn == rd and abs(add_imm - target_off) < 32:
                        print(f"MATCH at 0x{pc:x}:")
                        dis_start = max(0, i - 32)
                        dis_end = min(len(s_data), i + 64)
                        for insn in md.disasm(s_data[dis_start:dis_end], text_exec_va + dis_start):
                            m = "==> " if insn.address == pc else "    "
                            print(f"{m}0x{insn.address:x}: {insn.mnemonic:8s} {insn.op_str}")
