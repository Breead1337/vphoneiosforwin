import struct, capstone

kc = open('/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin', 'rb')
hdr = kc.read(0x4000)
ncmds = struct.unpack_from('<I', hdr, 16)[0]
off = 32
segs = []
for _ in range(ncmds):
    cmd, cmdsize = struct.unpack_from('<II', hdr, off)
    if cmd == 0x19:
        segname = hdr[off+8:off+24].rstrip(b'\x00').decode('latin1')
        vmaddr, vmsize, fileoff, filesize = struct.unpack_from('<QQQQ', hdr, off+24)
        segs.append((segname, vmaddr, vmsize, fileoff))
    off += cmdsize

target = 0xfffffe0008a60cfc
md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)

for sname, vm, sz, fo in segs:
    if 'TEXT' in sname:
        kc.seek(fo)
        data = kc.read(sz)
        for i in range(0, sz - 4, 4):
            word = struct.unpack_from('<I', data, i)[0]
            # B or BL
            if (word & 0x7c000000) == 0x14000000:
                imm26 = word & 0x03ffffff
                if imm26 & 0x02000000:
                    imm26 -= 0x04000000
                dest = vm + i + (imm26 << 2)
                if dest == target:
                    caller = vm + i
                    print(f"Branch to {target:#x} from {caller:#x}")
                    start = max(0, i - 32)
                    cdata = data[start:i+32]
                    for ins in md.disasm(cdata, vm + start):
                        prefix = "==> " if ins.address == caller else "    "
                        print(f"{prefix}{ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")
            # conditional branches B.cond
            elif (word & 0xff000010) == 0x54000000:
                imm19 = (word >> 5) & 0x7ffff
                if imm19 & 0x40000:
                    imm19 -= 0x80000
                dest = vm + i + (imm19 << 2)
                if dest == target:
                    caller = vm + i
                    print(f"Cond branch to {target:#x} from {caller:#x}")
