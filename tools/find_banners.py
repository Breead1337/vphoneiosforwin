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
            segs.append((segname, vmaddr, vmsize, fileoff, filesize))
        off += cmdsize

    def find_str(pattern):
        results = []
        for sname, vm, sz, fo, fs in segs:
            kc.seek(fo)
            data = kc.read(fs)
            idx = 0
            while True:
                idx = data.find(pattern.encode('latin1'), idx)
                if idx == -1: break
                results.append((sname, vm + idx))
                idx += len(pattern)
        return results

    # Find "Darwin Kernel Version" or "root device"
    print("Finding kernel banner strings...")
    for sname, va in find_str("Darwin Kernel Version"):
        print(f"  {va:#x} in {sname}")
    for sname, va in find_str("kprintf"):
        print(f"  'kprintf' at {va:#x} in {sname}")
