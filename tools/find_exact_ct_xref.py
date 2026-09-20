import struct
import capstone

kc_path = "/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin"

with open(kc_path, "rb") as f:
    data = f.read()

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

target_va = 0xfffffe00071f8234
target_page = target_va & ~0xfff
target_off = target_va & 0xfff

print(f"Target VA: 0x{target_va:x} (Page: 0x{target_page:x}, Off: 0x{target_off:x})")

md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)
md.detail = True

for segname, vmaddr, vmsize, fileoff, filesize in segments:
    if "TEXT" in segname:
        s_data = data[fileoff:fileoff + filesize]
        # Track ADRP registers
        # map rd -> (adrp_pc, page)
        adrp_regs = {}
        for i in range(0, len(s_data), 4):
            pc = vmaddr + i
            insn_val = struct.unpack_from("<I", s_data[i:i+4])[0]
            
            # ADRP
            if (insn_val & 0x9f000000) == 0x90000000:
                immlo = (insn_val >> 29) & 3
                immhi = (insn_val >> 5) & 0x7ffff
                imm = (immhi << 2) | immlo
                if imm & (1 << 20):
                    imm -= (1 << 21)
                adrp_page = (pc & ~0xfff) + (imm << 12)
                rd = insn_val & 0x1f
                adrp_regs[rd] = (pc, adrp_page)
                continue
            
            # ADD (imm)
            if (insn_val & 0x3fc00000) == 0x11000000:
                rd = insn_val & 0x1f
                rn = (insn_val >> 5) & 0x1f
                imm12 = (insn_val >> 10) & 0xfff
                if rn in adrp_regs:
                    adrp_pc, page = adrp_regs[rn]
                    final_va = page + imm12
                    if final_va == target_va:
                        print(f"FOUND MATCH: ADRP at 0x{adrp_pc:x}, ADD at 0x{pc:x} in {segname}!")
                        # Disassemble around pc
                        dis_start = max(0, i - 48)
                        dis_end = min(len(s_data), i + 48)
                        for insn in md.disasm(s_data[dis_start:dis_end], vmaddr + dis_start):
                            mark = ">> " if insn.address == pc else "   "
                            print(f"{mark}0x{insn.address:x}: {insn.mnemonic:8s} {insn.op_str}")
                continue

            # If register is overwritten, clear it
            # (simple check: if insn writes rd)
            # For simplicity, if distance > 32 bytes, let it expire
            to_del = [r for r, (apc, _) in adrp_regs.items() if pc - apc > 64]
            for r in to_del:
                del adrp_regs[r]

