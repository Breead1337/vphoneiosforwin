# dtpatch.py OUT.im4p — DeviceTree IM4P with /chosen/manifest-properties added.
# iBoot builds that node from the IM4M; we boot without one (LLB patch), so XNU's AppleImage4 panics
# "failed to init ignition blob: 2" (getProperty("ECID") -> ENOENT). Values mirror the config device.
#
# Also renames one /chosen/memory-map/MemoryMapReserved-N slot to "TrustCache" pointing at a
# fixed guest-phys buffer (loaded by overlay/hw/vmapple/vresearch101.c via $VR_TRUSTCACHE).
# XNU's AppleImage4/AMFI reads /chosen/memory-map/TrustCache as {u64 paddr, u64 size} — see
# "Unexpected /chosen/memory-map/TrustCache property size %u != %zu" in kernelcache strings.
import os, struct, sys
from mkaux import der

RAW = __file__.rsplit("tools", 1)[0] + "fw/cloud/raw/DeviceTree.vresearch101ap.bin"
MANIFEST = {"ECID": struct.pack("<Q", 0)}  # ponytail: only what XNU asked for so far; add keys as panics name them

# TrustCache load address in guest RAM — must match VR_TC_PADDR in vresearch101.c.
# Top 64 KiB of the default 4 GiB VR_MEM (0x70000000 + 4 GiB - 64 KiB); iBoot allocates
# bottom-up so this stays untouched (highest EL0 SP seen so far ~0x16f6a0000).
TC_PADDR = 0x16FFF0000
TC_PATH = os.environ.get("VR_TRUSTCACHE")  # raw trst payload (after `ipsw img4 im4p extract`)

# /chosen/boot-args — iBoot обычно берёт из NVRAM (у нас пустой). XNU читает
# CommandLine из BootArgs struct (не из DT), но некоторые подсистемы (kext_start,
# security policy) читают именно /chosen/boot-args. Оставляем пустым и добавляем
# только через $VR_BOOTARGS, чтобы не сломать существующий boot без нужды.
BOOTARGS = os.environ.get("VR_BOOTARGS")


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

tc_note = "skipped (VR_TRUSTCACHE unset)"
if TC_PATH:
    tc_size = os.path.getsize(TC_PATH)
    mm = next(k for k in chosen[1] if nodename(k) == b"memory-map")
    # Same rename trick as manifest-properties: pick the first free 16-byte MemoryMapReserved slot.
    # 16 bytes matches the memory-map entry layout {u64 paddr, u64 size} XNU expects.
    slot = next(i for i, q in enumerate(mm[0]) if q[0].startswith(b"MemoryMapReserved-") and q[1] == 16)
    mm[0][slot] = prop("TrustCache", struct.pack("<QQ", TC_PADDR, tc_size))
    tc_note = f"TrustCache @ {TC_PADDR:#x}+{tc_size:#x} (slot {mm[0][slot][0].rstrip(chr(0).encode())!r})"

ba_note = "boot-args skipped (VR_BOOTARGS unset)"
if BOOTARGS:
    ba_bytes = BOOTARGS.encode() + b"\0"
    # Add/replace /chosen/boot-args (property, not child node). name= is at index [0] of a prop tuple.
    existing = next((i for i, q in enumerate(chosen[0]) if q[0].rstrip(b"\0") == b"boot-args"), None)
    if existing is not None:
        chosen[0][existing] = prop("boot-args", ba_bytes)
    else:
        chosen[0].append(prop("boot-args", ba_bytes))
    ba_note = f"boot-args = {BOOTARGS!r}"

payload = ser(root) + d[end:]
open(sys.argv[1], "wb").write(der(0x30, der(0x16, b"IM4P") + der(0x16, b"dtre") + der(0x16, b"patched") + der(0x04, payload)))
print(f"dt {len(d):#x} -> {len(payload):#x}, chosen/manifest-properties: {list(MANIFEST)}, {tc_note}, {ba_note}")
