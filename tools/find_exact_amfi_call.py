import struct
import capstone

kc_path = "/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin"
with open(kc_path, "rb") as f:
    data = f.read()

target_va = 0xfffffe00071f8228
target_page = 0xfffffe00071f8000
target_off = 0x228

# Search in __TEXT_EXEC and __PRELINK_TEXT
segments = [
    ("__TEXT_EXEC", 0xfffffe0007a94000, 0x0183c000, 0x00a90000),
    ("__PRELINK_TEXT", 0xfffffe0007008000, 0x0067c000, 0x00004000)
]

md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)

for segname, vmaddr, vmsize, fileoff in segments:
    s_data = data[fileoff:fileoff + vmsize]
    print(f"Scanning {segname}...")
    for i in range(0, len(s_data) - 8, 4):
        insn_val = struct.unpack_from("<I", s_data[i:i+4])[0]
        if (insn_val & 0x9f000000) == 0x90000000: # ADRP
            immlo = (insn_val >> 29) & 3
            immhi = (insn_val >> 5) & 0x7ffff
            imm = (immhi << 2) | immlo
            if imm & (1 << 20): imm -= (1 << 21)
            pc = vmaddr + i
            adrp_page = (pc & ~0xfff) + (imm << 12)
            if adrp_page == target_page:
                rd = insn_val & 0x1f
                # check next instruction for add rd, rd, #0x228
                next_val = struct.unpack_from("<I", s_data[i+4:i+8])[0]
                if (next_val & 0x3fc00000) == 0x11000000: # ADD
                    add_imm = (next_val >> 10) & 0xfff
                    rn = (next_val >> 5) & 0x1f
                    if rn == rd and add_imm == target_off:
                        print(f"FOUND EXACT MATCH in {segname} at 0x{pc:x}!")
                        dis_start = max(0, i - 64)
                        dis_end = min(len(s_data), i + 128)
                        for insn in md.disasm(s_data[dis_start:dis_end], vmaddr + dis_start):
                            m = "==> " if insn.address == pc else "    "
                            print(f"{m}0x{insn.address:x}: {insn.mnemonic:8s} {insn.op_str}")

