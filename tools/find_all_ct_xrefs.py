import struct
import capstone

kc_path = "/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin"

with open(kc_path, "rb") as f:
    data = f.read()

# Let's find all occurrences of "unsuitable CT policy" or "CT policy" strings in the entire kernelcache
idx = 0
str_offsets = []
while True:
    idx = data.find(b"unsuitable CT policy", idx)
    if idx == -1:
        break
    str_offsets.append(idx)
    print(f"Found 'unsuitable CT policy' at offset 0x{idx:x}")
    idx += 1

# For each offset, find segment & VA
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

def file2va(foff):
    for segname, vmaddr, vmsize, fileoff, filesize in segments:
        if fileoff <= foff < fileoff + filesize:
            return vmaddr + (foff - fileoff)
    return None

str_vas = [file2va(soff) for soff in str_offsets]
print("String VAs:", [hex(v) for v in str_vas])

# Now search for ANY instruction in __TEXT_EXEC or __PRELINK_TEXT referencing these VAs
md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)

for segname, vmaddr, vmsize, fileoff, filesize in segments:
    if "TEXT" in segname:
        s_data = data[fileoff:fileoff + filesize]
        for sva in str_vas:
            spage = sva & ~0xfff
            spage_off = sva & 0xfff
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
                    if adrp_page == spage:
                        # Check following instructions (up to 4 insns ahead) for ADD or LDR with spage_off
                        for k in range(4, 20, 4):
                            if i + k + 4 > len(s_data): break
                            nval = struct.unpack_from("<I", s_data[i+k:i+k+4])[0]
                            # ADD imm: (nval & 0x3fc00000) == 0x11000000
                            if (nval & 0x3fc00000) == 0x11000000:
                                add_imm = (nval >> 10) & 0xfff
                                if add_imm == spage_off:
                                    print(f"MATCH xref at 0x{pc:x} in {segname}:")
                                    for insn in md.disasm(s_data[i:i+k+16], pc):
                                        print(f"  0x{insn.address:x}: {insn.mnemonic:8s} {insn.op_str}")
                                    break
