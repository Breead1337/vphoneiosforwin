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

md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)

targets = [0x8349c, 0x2884a4]
for t in targets:
    for sname, vm, sz, fo in segs:
        if fo <= t < fo + sz:
            va = vm + (t - fo)
            print(f"Offset {t:#x} -> VA {va:#x} in {sname}")
            page_va = va & ~0xfff
            page_off = va & 0xfff
            # search for ADRP + ADD
            for s2, vm2, sz2, fo2 in segs:
                if 'EXEC' in s2:
                    kc.seek(fo2)
                    data = kc.read(sz2)
                    for i in range(0, sz2 - 8, 4):
                        w0 = struct.unpack_from('<I', data, i)[0]
                        if (w0 & 0x9f000000) == 0x90000000:
                            immhi = (w0 >> 5) & 0x7ffff
                            immlo = (w0 >> 29) & 3
                            imm = (immhi << 2) | immlo
                            if imm & 0x100000: imm -= 0x200000
                            ins_va = vm2 + i
                            if (ins_va & ~0xfff) + (imm << 12) == page_va:
                                w1 = struct.unpack_from('<I', data, i + 4)[0]
                                if (w1 & 0x3b800000) == 0x11000000:
                                    if ((w1 >> 10) & 0xfff) == page_off:
                                        print(f"  XREF from {ins_va:#x} in {s2}:")
                                        kc.seek(fo2 + i - 16)
                                        code = kc.read(64)
                                        for ins in md.disasm(code, ins_va - 16):
                                            mark = "==> " if ins.address == ins_va else "    "
                                            print(f"    {mark}{ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")
