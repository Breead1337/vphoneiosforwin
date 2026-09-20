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

# MSR VBAR_EL1, Xt:
# System register encoding for VBAR_EL1: op0=3, op1=0, crn=12, crm=0, op2=0
# msr vbar_el1, x0 is: 1101 0101 0001 0000 1100 0000 0000 0000 -> 0xd518c000
# msr vbar_el1, xt -> (word & 0xffffff00) == 0xd518c000 or similar
# In AArch64: msr S3_0_C12_C0_0, Xt
# op0=3, op1=0, crn=12, crm=0, op2=0 -> 1101 0101 0001 1000 1100 0000 0000 0000 = 0xd518c000
md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)

for sname, vm, sz, fo in segs:
    if 'TEXT' in sname:
        kc.seek(fo)
        data = kc.read(sz)
        for i in range(0, sz - 4, 4):
            word = struct.unpack_from('<I', data, i)[0]
            if (word & 0xfffff000) == 0xd518c000:
                addr = vm + i
                start = max(0, i - 16)
                for ins in md.disasm(data[start:i+20], vm + start):
                    prefix = "==> " if ins.address == addr else "    "
                    print(f"{prefix}{ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")
                print()
