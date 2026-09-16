import sys, struct

# Let's write a small dtree walker
d = open(r"D:\vphonewin\fw\cloud\raw\DeviceTree.vresearch101ap.bin", "rb").read()

def parse_node(offset):
    # Apple DT format:
    # nprops (uint32), nchildren (uint32)
    # props: name (32 bytes), size (uint32), data (size bytes, rounded up to 4)
    # children...
    if offset >= len(d):
        return offset
    nprops, nchildren = struct.unpack_from("<II", d, offset)
    cur = offset + 8
    props = {}
    for _ in range(nprops):
        pname = d[cur:cur+32].split(b'\x00')[0].decode('latin1')
        psize = struct.unpack_from("<I", d, cur+32)[0]
        cur += 36
        pdata = d[cur:cur+psize]
        cur += (psize + 3) & ~3
        props[pname] = pdata
    name = props.get('name', b'').split(b'\x00')[0].decode('latin1', errors='ignore')
    if 'reg' in props:
        rdata = props['reg']
        regs = []
        # format depends on address-cells / size-cells, often 64-bit addr + 64-bit size
        if len(rdata) % 16 == 0:
            for i in range(0, len(rdata), 16):
                addr, size = struct.unpack_from("<QQ", rdata, i)
                regs.append((hex(addr), hex(size)))
        elif len(rdata) % 8 == 0:
            for i in range(0, len(rdata), 8):
                addr, size = struct.unpack_from("<II", rdata, i)
                regs.append((hex(addr), hex(size)))
        print(f"Node: {name} | props: {list(props.keys())} | reg: {regs}")
    for _ in range(nchildren):
        cur = parse_node(cur)
    return cur

parse_node(0)
