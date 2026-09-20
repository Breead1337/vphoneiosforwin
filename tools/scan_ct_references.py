import struct
import capstone

kc_path = "/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin"
with open(kc_path, "rb") as f:
    data = f.read()

target_va = 0xfffffe00071f8234
target_page = target_va & ~0xfff
target_off = target_va & 0xfff

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

# 1. Look for pointer in data sections
for segname, vmaddr, vmsize, fileoff, filesize in segments:
    s_data = data[fileoff:fileoff + filesize]
    ptr_bytes = struct.pack("<Q", target_va)
    idx = 0
    while True:
        idx = s_data.find(ptr_bytes, idx)
        if idx == -1: break
        print(f"Direct pointer to 0x{target_va:x} in {segname} at VA 0x{vmaddr + idx:x}")
        idx += 1

# 2. Look for any ADRP to target_page in ANY executable segment
md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)
for segname, vmaddr, vmsize, fileoff, filesize in segments:
    if "TEXT" in segname:
        s_data = data[fileoff:fileoff + filesize]
        for i in range(0, len(s_data) - 4, 4):
            insn_val = struct.unpack_from("<I", s_data[i:i+4])[0]
            if (insn_val & 0x9f000000) == 0x90000000: # ADRP
                immlo = (insn_val >> 29) & 3
                immhi = (insn_val >> 5) & 0x7ffff
                imm = (immhi << 2) | immlo
                if imm & (1 << 20): imm -= (1 << 21)
                pc = vmaddr + i
                adrp_page = (pc & ~0xfff) + (imm << 12)
                if adrp_page == target_page:
                    # Check next 8 instructions for any use of target_off or rd
                    rd = insn_val & 0x1f
                    chunk = s_data[i:min(len(s_data), i + 36)]
                    dis = list(md.disasm(chunk, pc))
                    found_off = False
                    for insn in dis:
                        if hex(target_off) in insn.op_str:
                            found_off = True
                            break
                    if found_off:
                        print(f"Found ADRP+target_off in {segname} at 0x{pc:x}:")
                        for insn in dis:
                            print(f"  0x{insn.address:x}: {insn.mnemonic:8s} {insn.op_str}")
