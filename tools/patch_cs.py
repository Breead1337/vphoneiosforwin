#!/usr/bin/env python3
# patch_cs.py — read a Mach-O with adhoc LC_CODE_SIGNATURE, apply an entry stub
# (mov w0,#0; ret @LC_MAIN entryoff), recompute the affected page SHA256 hash
# slot and the CodeDirectory blob's own SHA256[0:20] (CDHash). Output: new
# Mach-O, printed new CDHash. Used to spawn "fake exit-0" binaries for missing
# hardwired boot tasks (session 50).
import hashlib, struct, sys

def read_len(buf, o):
    b = buf[o]; o += 1
    if b & 0x80:
        n = b & 0x7f
        return int.from_bytes(buf[o:o+n], 'big'), o + n
    return b, o

def stub_entry(d, entryoff):
    """Overwrite `mov w0, #0; ret` at entryoff. Returns modified bytes."""
    d = bytearray(d)
    d[entryoff:entryoff+8] = struct.pack('<II', 0x52800000, 0xd65f03c0)
    return bytes(d)

def find_cs(d):
    """Return (LC_CODE_SIGNATURE dataoff, datasize, LC_MAIN entryoff)."""
    ncmds = struct.unpack_from('<I', d, 16)[0]
    o = 32
    entryoff = None
    csoff = None
    cssize = None
    for _ in range(ncmds):
        cmd, cmdsize = struct.unpack_from('<II', d, o)
        if cmd == 0x1d:  # LC_CODE_SIGNATURE
            csoff, cssize = struct.unpack_from('<II', d, o+8)
        elif cmd == 0x80000028:  # LC_MAIN
            entryoff, _ = struct.unpack_from('<QQ', d, o+8)
        o += cmdsize
    return csoff, cssize, entryoff

def recompute_cd(d, csoff, cssize):
    """Update the code hash slots of the CD blob in-place, then recompute CDHash."""
    d = bytearray(d)
    cs = d[csoff:csoff+cssize]
    magic, length, count = struct.unpack('>III', cs[:12])
    assert magic == 0xFADE0CC0
    for i in range(count):
        btype, boff = struct.unpack('>II', cs[12+i*8:12+i*8+8])
        bmagic = struct.unpack('>I', cs[boff:boff+4])[0]
        if bmagic == 0xFADE0C02:
            m, ln, ver, flags, hOff, iOff, nSpec, nCode, cLim, hSize, hType, plat, pgSz, spare = struct.unpack('>IIIIIIIIIBBBBI', cs[boff:boff+44])
            assert hSize == 32 and hType == 2 and pgSz == 12, 'expect SHA256 / 4KB pages'
            page_size = 1 << pgSz
            # rewrite each code page slot (only page 0 changed in practice, but do all — cheap)
            for j in range(nCode):
                start = j * page_size
                end = min(start + page_size, cLim)
                h = hashlib.sha256(d[start:end]).digest()
                slot_off = csoff + boff + hOff + j * hSize
                d[slot_off:slot_off + hSize] = h
            # recompute CDHash = SHA256(CD blob)[0:20]
            new_cs = bytes(d[csoff:csoff+cssize])
            cd_bytes = new_cs[boff:boff+ln]
            cdhash = hashlib.sha256(cd_bytes).digest()[:20]
            return bytes(d), cdhash
    raise RuntimeError('CodeDirectory blob not found')

def process(src, dst):
    d = open(src, 'rb').read()
    csoff, cssize, entryoff = find_cs(d)
    if entryoff is None or csoff is None:
        raise SystemExit(f'{src}: LC_CODE_SIGNATURE or LC_MAIN missing')
    d = stub_entry(d, entryoff)
    d, cdhash = recompute_cd(d, csoff, cssize)
    open(dst, 'wb').write(d)
    return cdhash

if __name__ == '__main__':
    src, dst = sys.argv[1], sys.argv[2]
    cdhash = process(src, dst)
    print(f'{dst}: CDHash = {cdhash.hex()}')
