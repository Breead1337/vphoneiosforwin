import struct

kc = open('fw/cloud/raw/kernelcache.research.vresearch101.bin', 'rb')
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

def read_str(addr):
    for sname, vm, sz, fo in segs:
        if vm <= addr < vm + sz:
            kc.seek(fo + (addr - vm))
            s = kc.read(128).split(b'\x00')[0]
            print(f'{addr:#x} ({sname}): {s}')
            return
    print(f'{addr:#x}: not found')

read_str(0xfffffe000760676d)
read_str(0xfffffe0007607966)
read_str(0xfffffe00076067d0)
read_str(0xfffffe0007606778)
