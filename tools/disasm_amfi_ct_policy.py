import struct
import capstone

kc_path = "/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin"

with open(kc_path, "rb") as f:
    data = f.read()

# Target VAs:
# 0xfffffe00071f8234: "unsuitable CT policy..."
# 0xfffffe00071f8453: "is adhoc signed"
# 0xfffffe00071f7d05: "code signature validation failed"

# We search in __TEXT_EXEC: vmaddr=0xfffffe0007a94000, fileoff=0x00a90000, size=0x0183c000
# and __PRELINK_TEXT: vmaddr=0xfffffe0007008000, fileoff=0x0004000, size=0x0067c000

md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)
md.detail = True

def search_xrefs(target_va):
    target_page = target_va & ~0xfff
    target_page_off = target_va & 0xfff
    print(f"\n=== Searching xrefs to VA 0x{target_va:x} (Page: 0x{target_page:x}, PageOff: 0x{target_page_off:x}) ===")
    
    # Check __TEXT_EXEC
    text_exec_va = 0xfffffe0007a94000
    text_exec_off = 0x00a90000
    text_exec_sz = 0x0183c000
    text_data = data[text_exec_off:text_exec_off + text_exec_sz]
    
    # Simple ADRP scanner
    for i in range(0, len(text_data) - 8, 4):
        insn_bytes = text_data[i:i+4]
        insn_val = struct.unpack_from("<I", insn_bytes)[0]
        # ADRP check: (insn_val & 0x9f000000) == 0x90000000
        if (insn_val & 0x9f000000) == 0x90000000:
            immlo = (insn_val >> 29) & 3
            immhi = (insn_val >> 5) & 0x7ffff
            imm = (immhi << 2) | immlo
            if imm & (1 << 20):
                imm -= (1 << 21)
            pc = text_exec_va + i
            adrp_page = (pc & ~0xfff) + (imm << 12)
            if adrp_page == target_page:
                rd = insn_val & 0x1f
                # check next instruction for ADD rd, rd, #page_off or LDR
                next_val = struct.unpack_from("<I", text_data[i+4:i+8])[0]
                # ADD (immediate): (next_val & 0xffc00000) == 0x91000000 (64-bit) or 0x11000000 (32-bit)
                if (next_val & 0x3fc00000) == 0x11000000:
                    add_imm = (next_val >> 10) & 0xfff
                    rn = (next_val >> 5) & 0x1f
                    if rn == rd and add_imm == target_page_off:
                        print(f"Match ADRP+ADD at 0x{pc:x} (file off 0x{text_exec_off + i:x})")
                        # Disassemble around this PC
                        dis_start = max(0, i - 64)
                        dis_end = min(len(text_data), i + 128)
                        for insn in md.disasm(text_data[dis_start:dis_end], text_exec_va + dis_start):
                            mark = "==> " if insn.address == pc else "    "
                            print(f"{mark}0x{insn.address:x}:  {insn.mnemonic:8s} {insn.op_str}")

search_xrefs(0xfffffe00071f8234)
search_xrefs(0xfffffe00071f8453)
search_xrefs(0xfffffe00071f7d05)
