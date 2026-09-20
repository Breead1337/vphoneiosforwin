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

# Convert file offsets to vmaddrs
# 0x1f3d05, 0x1f4234, 0x89990
targets = [0x1f3d05, 0x1f4234, 0x89990]
target_vms = []
for t in targets:
    for sname, vm, sz, fo in segs:
        if fo <= t < fo + sz:
            va = vm + (t - fo)
            target_vms.append((t, va, sname))
            print(f"File offset {t:#x} -> VA {va:#x} in {sname}")
            break

md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)

# Search for ADRP + ADD pointing to these VAs across all executable segments
for fo_t, va_t, sname_t in target_vms:
    page_va = va_t & ~0xfff
    page_off = va_t & 0xfff
    print(f"\nSearching xrefs to VA {va_t:#x} (page {page_va:#x}, off {page_off:#x}):")
    for sname, vm, sz, fo in segs:
        if 'EXEC' in sname or 'TEXT' in sname:
            kc.seek(fo)
            data = kc.read(sz)
            for i in range(0, sz - 8, 4):
                # check ADRP
                w0 = struct.unpack_from('<I', data, i)[0]
                if (w0 & 0x9f000000) == 0x90000000: # ADRP
                    # decode ADRP target
                    immhi = (w0 >> 5) & 0x7ffff
                    immlo = (w0 >> 29) & 3
                    imm = (immhi << 2) | immlo
                    if imm & 0x100000: imm -= 0x200000
                    ins_va = vm + i
                    adrp_dest = (ins_va & ~0xfff) + (imm << 12)
                    if adrp_dest == page_va:
                        # check next instruction for ADD or LDR
                        w1 = struct.unpack_from('<I', data, i + 4)[0]
                        # ADD (imm): 0x91000000
                        if (w1 & 0x3b800000) == 0x11000000:
                            add_imm = (w1 >> 10) & 0xfff
                            if add_imm == page_off:
                                print(f"  Match at {ins_va:#x} in {sname}!")
                                # disassemble around it
                                kc.seek(fo + i - 16)
                                chunk = kc.read(48)
                                for ins in md.disasm(chunk, ins_va - 16):
                                    mark = "==> " if ins.address == ins_va else "    "
                                    print(f"    {mark}{ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")
