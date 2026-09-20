import struct

kc_path = "/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin"
with open(kc_path, "rb") as f:
    data = f.read()

target_va = 0xfffffe0007d520c0
# PAC-signed pointers have top 16 bits non-zero or masked
target_lo48 = target_va & 0x0000ffffffffffff

print(f"Searching 8-byte pointers matching 0x{target_lo48:x} in kernelcache...")
for i in range(0, len(data) - 8, 8):
    val = struct.unpack_from("<Q", data[i:i+8])[0]
    if (val & 0x0000ffffffffffff) == target_lo48:
        print(f"Found pointer at file offset 0x{i:x}: raw value 0x{val:016x}")

# Also search for ADRP + ADD pointing to 0x7d520c0
import capstone
md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)
text_exec_va = 0xfffffe0007a94000
text_exec_off = 0x00a90000
text_exec_sz = 0x0183c000
s_data = data[text_exec_off:text_exec_off + text_exec_sz]
target_page = target_va & ~0xfff
target_off = target_va & 0xfff

print("Searching ADRP+ADD...")
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
                if rn == rd and add_imm == target_off:
                    print(f"ADRP+ADD at 0x{pc:x}")
