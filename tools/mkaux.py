# build aux.img: IMG4 containers (no IM4M) laid out back to back, as LLB scans them
# usage (WSL): python3 mkaux.py out.img [align=1]; NVRAM region (0xa00000..) is written by LLB itself
import sys

FW = "/mnt/d/vphonewin/fw/cloud/Firmware/"
IMAGES = [  # order matters: AVPBooter takes the first one (illb)
    FW + "all_flash/LLB.vresearch101.RELEASE.im4p",
    FW + "all_flash/iBoot.vresearch101.RESEARCH_RELEASE.im4p",
]


def der_len(n):
    if n < 0x80:
        return bytes([n])
    b = n.to_bytes((n.bit_length() + 7) // 8, "big")
    return bytes([0x80 | len(b)]) + b


def img4(im4p):
    body = b"\x16\x04IMG4" + im4p
    return b"\x30" + der_len(len(body)) + body


if __name__ == "__main__":
    out = sys.argv[1]
    ALIGN = int(sys.argv[2]) if len(sys.argv) > 2 else 1  # LLB reads the next header right at off+len
    size = 128 << 20
    buf = bytearray(size)
    off = 0
    for p in IMAGES:
        c = img4(open(p, "rb").read())
        assert off + len(c) < 0xa00000, "images overlap NVRAM"
        buf[off:off + len(c)] = c
        print(f"{p.split('/')[-1]} tag={c[c.find(b'IM4P') + 6:c.find(b'IM4P') + 10]} @ {off:#x} len {len(c):#x}")
        off = (off + len(c) + ALIGN - 1) & -ALIGN
    open(out, "wb").write(buf)
