# sysregs.py FILE [base-for-raw] — histogram of msr/mrs/sys/gxf instrs in Mach-O exec segments or raw blob
import sys, struct, collections, capstone
f = sys.argv[1]; d = open(f, 'rb').read()
segs = []
if d[:4] == b'\xcf\xfa\xed\xfe':
    ncmds = struct.unpack('<I', d[16:20])[0]; o = 32
    for _ in range(ncmds):
        cmd, sz = struct.unpack('<II', d[o:o+8])
        if cmd == 0x19:
            name = d[o+8:o+24].rstrip(b'\0').decode(); vm, vs, fo, fs, mp, ip = struct.unpack('<QQQQII', d[o+24:o+64])
            if ip & 4 and fs: segs.append((name, vm, d[fo:fo+fs]))
        o += sz
else:
    segs.append(('raw', int(sys.argv[2], 0) if len(sys.argv) > 2 else 0, d))
md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM); md.skipdata = True
c = collections.Counter(); first = {}
for name, vm, blob in segs:
    for off in range(0, len(blob) - 3, 4):
        w = struct.unpack('<I', blob[off:off+4])[0]
        if (w & 0xffc00000) == 0xd5000000 or w in (0x00201420, 0x00201400):
            if w == 0x00201420: k = 'GENTER'
            elif w == 0x00201400: k = 'GEXIT'
            else:
                ins = next(md.disasm(blob[off:off+4], vm+off), None)
                if not ins: continue
                if ins.mnemonic in ('nop','dsb','isb','dmb','hint','sev','wfe','wfi','yield','bti','pacibsp','autibsp','paciasp','autiasp','xpaclri','clrex','sb','esb','csdb','pssbb','ssbb'): continue
                k = ins.mnemonic + ' ' + (ins.op_str.split(',')[0] if ins.mnemonic=='msr' else ins.op_str.split(', ')[-1])
            c[k] += 1; first.setdefault(k, vm+off)
for k, n in sorted(c.items(), key=lambda x: x[0]): print(f'{n:5d} {first[k]:#x} {k}')
