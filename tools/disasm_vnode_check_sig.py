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

# In __PRELINK_TEXT (or where AMFI code is):
# Where is AMFI code?
# Earlier in tools/run_userspace.sh:
# vnode_check_signature is at 0xfffffe0007d5785c!
# Let's disassemble around 0xfffffe0007d56dd4 (vnode_check_signature) to 0x7d57860!
target = 0xfffffe0007d56dd4
for sname, vm, sz, fo in segs:
    if vm <= target < vm + sz:
        kc.seek(fo + (target - vm))
        code = kc.read(0xb00)
        print(f"Disassembly of vnode_check_signature ({target:#x}):")
        for ins in md.disasm(code, target):
            # look for adrp/add or bl
            if ins.mnemonic in ('adrp', 'adr', 'bl', 'blraa', 'retab', 'ret') or '0x71f7' in ins.op_str or '0x71f8' in ins.op_str:
                print(f"  {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")
        break
