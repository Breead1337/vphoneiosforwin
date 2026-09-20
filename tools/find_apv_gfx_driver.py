import struct
import capstone

kc_path = "/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin"
with open(kc_path, "rb") as f:
    data = f.read()

text_exec_va = 0xfffffe0007a94000
text_exec_off = 0x00a90000
text_exec_sz = 0x0183c000
s_data = data[text_exec_off:text_exec_off + text_exec_sz]

md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)

# Search for ldr/str with offset 0x1034 or 0x1014 or 0x1018
for i in range(0, len(s_data) - 4, 4):
    insn_val = struct.unpack_from("<I", s_data[i:i+4])[0]
    # LDR/STR unsigned immediate: (insn_val & 0xbfc00000) == 0xb9400000
    # For size 4: imm12 = (insn_val >> 10) & 0xfff -> imm = imm12 * 4
    if (insn_val & 0xbfc00000) == 0xb9000000 or (insn_val & 0xbfc00000) == 0xb9400000:
        imm12 = (insn_val >> 10) & 0xfff
        if imm12 * 4 == 0x1034:
            pc = text_exec_va + i
            print(f"Match 0x1034 at 0x{pc:x}")
            for insn in md.disasm(s_data[max(0, i-32):min(len(s_data), i+32)], pc - 32):
                m = "==> " if insn.address == pc else "    "
                print(f"{m}0x{insn.address:x}: {insn.mnemonic:8s} {insn.op_str}")
            break
