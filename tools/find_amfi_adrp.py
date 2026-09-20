import struct

kc_path = "/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin"

with open(kc_path, "rb") as f:
    data = f.read()

# 1. Search raw 64-bit pointer
targets = [
    0xfffffe00071f8234, # unsuitable CT policy
    0xfffffe00071f8453, # is adhoc signed
    0xfffffe00071f7d05, # code signature validation failed
    0xfffffe00071f8000, # page
]

for t in targets:
    b = struct.pack("<Q", t)
    idx = 0
    while True:
        idx = data.find(b, idx)
        if idx == -1:
            break
        print(f"Found pointer 0x{t:x} at file offset 0x{idx:x}")
        idx += len(b)

# 2. Search ANY ADRP targeting page 0xfffffe00071f8000 or 0xfffffe00071f7000
# Parse segments to get VA
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

target_pages = [0xfffffe00071f8000, 0xfffffe00071f7000]

for segname, vmaddr, vmsize, fileoff, filesize in segments:
    if "TEXT" in segname:
        s_data = data[fileoff:fileoff + filesize]
        for i in range(0, len(s_data), 4):
            insn_val = struct.unpack_from("<I", s_data[i:i+4])[0]
            if (insn_val & 0x9f000000) == 0x90000000: # ADRP
                immlo = (insn_val >> 29) & 3
                immhi = (insn_val >> 5) & 0x7ffff
                imm = (immhi << 2) | immlo
                if imm & (1 << 20):
                    imm -= (1 << 21)
                pc = vmaddr + i
                adrp_page = (pc & ~0xfff) + (imm << 12)
                if adrp_page in target_pages:
                    rd = insn_val & 0x1f
                    print(f"ADRP in {segname} at 0x{pc:x} (x{rd}, page 0x{adrp_page:x})")
