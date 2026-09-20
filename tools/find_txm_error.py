import struct
import capstone

kc_path = "/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin"

with open(kc_path, "rb") as f:
    data = f.read()

# File offset 0x89990 -> VA 0xfffffe000708d990
# Let's see the string around 0x89990
print("String at 0x89990:", data[0x89990:0x89990+80])

# Search for xrefs to 0xfffffe000708d990
target_va = 0xfffffe000708d990
target_page = target_va & ~0xfff
target_page_off = target_va & 0xfff

# Parse segments
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

for segname, vmaddr, vmsize, fileoff, filesize in segments:
    if "TEXT" in segname:
        s_data = data[fileoff:fileoff + filesize]
        for i in range(0, len(s_data) - 4, 4):
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
                    print(f"ADRP to 0x{target_page:x} at 0x{pc:x} in {segname}")
                    for insn in md.disasm(s_data[i:i+32], pc):
                        print(f"  0x{insn.address:x}: {insn.mnemonic:8s} {insn.op_str}")
                    break
