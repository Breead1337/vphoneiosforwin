# dtpatch.py OUT.im4p — DeviceTree IM4P with /chosen/manifest-properties added.
# iBoot builds that node from the IM4M; we boot without one (LLB patch), so XNU's AppleImage4 panics
# "failed to init ignition blob: 2" (getProperty("ECID") -> ENOENT). Values mirror the config device.
import struct, sys
from mkaux import der

RAW = __file__.rsplit("tools", 1)[0] + "fw/cloud/raw/DeviceTree.vresearch101ap.bin"
MANIFEST = {"ECID": struct.pack("<Q", 0)}  # ponytail: only what XNU asked for so far; add keys as panics name them


def parse(d, o):
    nprops, nkids = struct.unpack_from("<II", d, o); o += 8
    props = []
    for _ in range(nprops):
        name = d[o:o + 32]; size = struct.unpack_from("<I", d, o + 32)[0]; o += 36
        props.append((name, size, d[o:o + (size & 0x7fffffff)])); o += ((size & 0x7fffffff) + 3) & ~3
    kids = []
    for _ in range(nkids):
        k, o = parse(d, o); kids.append(k)
    return (props, kids), o


def ser(node):
    props, kids = node
    out = struct.pack("<II", len(props), len(kids))
    for name, size, data in props:
        out += name + struct.pack("<I", size) + data + b"\0" * (-len(data) % 4)
    return out + b"".join(ser(k) for k in kids)


def prop(name, data):
    return (name.encode().ljust(32, b"\0"), len(data), data)


def nodename(n):
    return next((p[2].split(b"\0")[0] for p in n[0] if p[0].rstrip(b"\0") == b"name"), b"")


d = open(RAW, "rb").read()
root, end = parse(d, 0)
assert ser(root) == d[:end], "round-trip mismatch"
chosen = next(k for k in root[1] if nodename(k) == b"chosen")
mp = next(k for k in chosen[1] if nodename(k) == b"manifest-properties")
spare = [i for i, q in enumerate(mp[0]) if q[0].startswith(b"UnusedIntegerProperty")]
for (key, val), i in zip(MANIFEST.items(), spare):  # iBoot renames these 8-byte placeholders the same way
    mp[0][i] = prop(key, val)
payload = ser(root) + d[end:]
open(sys.argv[1], "wb").write(der(0x30, der(0x16, b"IM4P") + der(0x16, b"dtre") + der(0x16, b"patched") + der(0x04, payload)))
print(f"dt {len(d):#x} -> {len(payload):#x}, chosen/manifest-properties: {list(MANIFEST)}")
