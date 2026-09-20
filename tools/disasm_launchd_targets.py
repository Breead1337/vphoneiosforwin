import struct, capstone

f = open('/home/ard/vrwork/launchd', 'rb')
hdr = f.read(0x4000)
ncmds = struct.unpack_from('<I', hdr, 16)[0]
off = 32
segs = []
for _ in range(ncmds):
    cmd, cmdsize = struct.unpack_from('<II', hdr, off)
    if cmd == 0x19: # LC_SEGMENT_64
        segname = hdr[off+8:off+24].rstrip(b'\x00').decode('latin1')
        vmaddr, vmsize, fileoff, filesize = struct.unpack_from('<QQQQ', hdr, off+24)
        segs.append((segname, vmaddr, vmsize, fileoff))
    off += cmdsize

print("launchd segments:")
for s in segs:
    print(f"  {s[0]:16s}: vmaddr={s[1]:#x} vmsize={s[2]:#x} fileoff={s[3]:#x}")

md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)

targets = [0x1182c4, 0x105aac, 0x105438, 0x103294, 0x1032ac, 0x1032bc, 0x1032cc, 0x1032dc, 0x10057c, 0x104310, 0x103230, 0x107ea0, 0x103228, 0x103218]

for target in sorted(targets):
    file_offset = target - 0x100000
    if 0 <= file_offset < 0x78000:
        f.seek(file_offset - 16)
        code = f.read(36)
        print(f"\n=======================================================")
        print(f"Disassembly around {target:#x} (file offset {file_offset:#x}) in __TEXT:")
        for ins in md.disasm(code, target - 16):
            prefix = "==> " if ins.address == target else "    "
            print(f"{prefix}{ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")
