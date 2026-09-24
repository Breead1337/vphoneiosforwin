#!/usr/bin/env python3
# Minimal Apple DeviceTree parser: dump the 'filesystems'/'fstab' subtree with property values.
import struct, sys
d = open(sys.argv[1] if len(sys.argv) > 1 else
         "/mnt/d/vphonewin/fw/cloud/raw/DeviceTree.vresearch101ap.bin", "rb").read()

pos = 0
def parse_node(depth, want):
    global pos
    nprop, nchild = struct.unpack_from("<II", d, pos); pos += 8
    props = {}
    name = None
    for _ in range(nprop):
        pname = d[pos:pos+32].split(b"\0")[0].decode("latin1"); pos += 32
        plen = struct.unpack_from("<I", d, pos)[0] & 0x7fffffff; pos += 4
        pdata = d[pos:pos+plen]; pos += (plen + 3) & ~3
        props[pname] = pdata
        if pname == "name":
            name = pdata.split(b"\0")[0].decode("latin1")
    show = want or name in ("filesystems", "fstab") or (name and ("fstab" in (name or "")))
    childwant = want or name in ("filesystems", "fstab")
    if show:
        ind = "  " * depth
        print(f"{ind}NODE name={name!r} props={nprop} children={nchild}")
        for k, v in props.items():
            if k == "name": continue
            # try to render as int if 4 bytes, else ascii/hex
            if len(v) == 4:
                iv = struct.unpack("<I", v)[0]
                print(f"{ind}  {k} = 0x{iv:x} ({iv})")
            else:
                txt = v.split(b'\0')[0]
                try: t = txt.decode('ascii'); r = repr(t) if t.isprintable() else v[:32].hex()
                except: r = v[:32].hex()
                print(f"{ind}  {k} = {r}  [{len(v)}B]")
    for _ in range(nchild):
        parse_node(depth+1, childwant)

parse_node(0, False)
