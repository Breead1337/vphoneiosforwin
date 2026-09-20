import struct, capstone

kc_path = '/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin'
with open(kc_path, 'rb') as kc:
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

    # In 0xfffffe00095270b0: 0x80002abe022d0014
    # Notice: 0x8000 is PAC discriminant / flags, 2abe is PAC salt!
    # The address is 0xfffffe0000000000 + 0x022d0014 = 0xfffffe00022d0014?
    # Or 0xfffffe0007000000 + 0x022d0014 = 0xfffffe00092d0014!
    # WOW: 0xfffffe0007000000 + 0x022d0014 = 0xfffffe00092d0014!
    # And look at what is at 0xfffffe00092d0014:
    # 0xfffffe00092d0014: mov x0, x1; b #0xfffffe00092d4000!
    # Let's check 0xfffffe00095270b0 .. 0xfffffe00095270c0
    kc.seek(0)
    for sname, vm, sz, fo in segs:
        if vm <= 0xfffffe00095270b0 < vm + sz:
            kc.seek(fo + (0xfffffe00095270b0 - vm))
            ptrs = struct.unpack('<QQQQ', kc.read(32))
            for i, p in enumerate(ptrs):
                print(f"Table ptr[{i}]: {p:#018x} -> {0xfffffe0007000000 + (p & 0xffffffff):#018x}")

    # Let's also check what 0xfffffe00092d4a6c does
    # 0xfffffe00092d4a6c: ldr x8, [x21], #8
    # x21 starts at 0xfffffe00095270b0
    # x20 is 0xfffffe00095270b8
    # So there is only ONE entry in this table: 0xfffffe00092d0014!
    # And at 0xfffffe00092d0014:
    #   mov x0, x1
    #   b 0xfffffe00092d4000
    # Wait, what was passed in x0 and x1?
    # 0xfffffe00092d4a70: add x0, x19, #0x6c
    # wait, x1 is NOT set! What was in x1?
    # Let's check 0xfffffe00092d4a50..0xfffffe00092d4a80
