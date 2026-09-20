import struct
import capstone

kc_path = "/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin"

with open(kc_path, "rb") as f:
    data = f.read()

# Parse Mach-O segments
segments = []
offset = 32
ncmds, sizeofcmds = struct.unpack_from("<II", data, 16)
for _ in range(ncmds):
    cmd, cmdsize = struct.unpack_from("<II", data, offset)
    if cmd == 0x19:
        segname = data[offset+8:offset+24].split(b'\0')[0].decode('ascii', errors='ignore')
        vmaddr, vmsize, fileoff, filesize = struct.unpack_from("<QQQQ", data, offset+24)
        segments.append((segname, vmaddr, vmsize, fileoff, filesize))
    offset += cmdsize

md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)
md.detail = True

def search_xrefs_in_segment(segname, target_va):
    target_page = target_va & ~0xfff
    target_page_off = target_va & 0xfff
    for sname, vmaddr, vmsize, fileoff, filesize in segments:
        if sname == segname:
            s_data = data[fileoff:fileoff + filesize]
            print(f"Scanning segment {segname} (VA 0x{vmaddr:x}..0x{vmaddr+vmsize:x}) for target VA 0x{target_va:x}...")
            for i in range(0, len(s_data) - 8, 4):
                insn_val = struct.unpack_from("<I", s_data[i:i+4])[0]
                if (insn_val & 0x9f000000) == 0x90000000: # ADRP
                    immlo = (insn_val >> 29) & 3
                    immhi = (insn_val >> 5) & 0x7ffff
                    imm = (immhi << 2) | immlo
                    if imm & (1 << 20):
                        imm -= (1 << 21)
                    pc = vmaddr + i
                    adrp_page = (pc & ~0xfff) + (imm << 12)
                    if adrp_page == target_page:
                        rd = insn_val & 0x1f
                        next_val = struct.unpack_from("<I", s_data[i+4:i+8])[0]
                        if (next_val & 0x3fc00000) == 0x11000000: # ADD
                            add_imm = (next_val >> 10) & 0xfff
                            rn = (next_val >> 5) & 0x1f
                            if rn == rd and add_imm == target_page_off:
                                print(f"==> MATCH in {segname} at 0x{pc:x} (file off 0x{fileoff + i:x})")
                                dis_start = max(0, i - 48)
                                dis_end = min(len(s_data), i + 80)
                                for insn in md.disasm(s_data[dis_start:dis_end], vmaddr + dis_start):
                                    m = ">>> " if insn.address == pc else "    "
                                    print(f"{m}0x{insn.address:x}: {insn.mnemonic:8s} {insn.op_str}")

# Strings:
# 0xfffffe00071f8234: "unsuitable CT policy %d for this platform/device, rejecting signature."
# 0xfffffe00071f8453: "is adhoc signed"
# 0xfffffe00071f7d05: "code signature validation failed"

search_xrefs_in_segment("__PRELINK_TEXT", 0xfffffe00071f8234)
search_xrefs_in_segment("__PRELINK_TEXT", 0xfffffe00071f8453)
search_xrefs_in_segment("__PRELINK_TEXT", 0xfffffe00071f7d05)
