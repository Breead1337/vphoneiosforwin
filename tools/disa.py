# disa.py FILE VA [COUNT] — disassemble a Mach-O (or fileset) by virtual address; capstone skipdata
import sys, struct, capstone
f, va, n = sys.argv[1], int(sys.argv[2], 0), int(sys.argv[3], 0) if len(sys.argv) > 3 else 64
d = open(f, 'rb').read()

def segs(d, base=0):
    ncmds = struct.unpack('<I', d[base+16:base+20])[0]; o = base + 32
    for _ in range(ncmds):
        cmd, sz = struct.unpack('<II', d[o:o+8])
        if cmd == 0x19:
            vm, vs, fo, fs = struct.unpack('<QQQQ', d[o+24:o+56])
            yield vm, fs, fo
        o += sz

fo = next((fo + va - vm for vm, fs, fo in segs(d) if vm <= va < vm + fs), None)
if fo is None: sys.exit(f'{va:#x} not in any segment')
md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM); md.skipdata = True
for i in md.disasm(d[fo:fo+n*4], va):
    print(f'{i.address:#x}: {i.mnemonic} {i.op_str}')
