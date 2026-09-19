# build aux.img: IMG4 containers (no IM4M) laid out back to back, as LLB scans them
# usage (WSL): python3 mkaux.py out.img [align=1]; NVRAM region (0xa00000..) is written by LLB itself
import struct, sys

FW = "/mnt/d/vphonewin/fw/cloud/Firmware/"
RAW = "/mnt/d/vphonewin/fw/cloud/raw/"
LLB_BASE = 0x7006C000
IBOOT_BASE = 0x7006C000  # ponytail: используется как якорь для file-offset патчей;
                          # реальный runtime base у iBoot может отличаться, но offsets те же
NOP = 0xD503201F
MOV_W0_0 = 0x52800000     # mov w0, #0 — заставить cbz w0, skip срабатывать всегда


def b(src, dst):
    return 0x14000000 | (((dst - src) >> 2) & 0x3FFFFFF)


# LLB (iBoot-13822.100.791.502.1) patches: va -> (orig insn, new insn)
# rootfs/panic sites found with vphone-cli research/iboot_patches.md anchors (their 26.3 VAs differ from 26.4)
LLB_PATCHES = {
    # image4 loader: IM4M missing -> tbz to 0x40040007 error; jump to payload extraction instead (same as AVPBooter 0x101640)
    0x70074348: (0x36000BC8, b(0x70074348, 0x70074770)),  # tbz w8,#0,0x700744c0 -> b payload extraction
    0x700A2A1C: (0x34000100, b(0x700A2A1C, 0x700A2A3C)),  # 4a rootfs: cbz w0 -> b (err 0x3b7)
    0x700A26F0: (0x54000AC2, NOP),                        # 4b rootfs: b.hs after cmp x8,#0x400
    0x700A2A64: (0x34FFEE60, b(0x700A2A64, 0x700A2830)),  # 4c rootfs: cbz w0 -> b (err 0x3c2)
    0x700A6608: (0xB4000268, NOP),                        # 4d rootfs: cbz x8 after ldr x8,[x22,#0x78]
    0x700A67C8: (0x340000C0, b(0x700A67C8, 0x700A67E0)),  # 4e rootfs: cbz w0 -> b (err 0x110)
    0x7008635C: (0x35000460, NOP),                        # 5 panic bypass: cbnz w0 after 0x400328 poke
}

# iBoot патчи (session 49): наш patched kernelcache имеет другой SHA-hash чем
# manifest в IM4M — iBoot валидатор говорит "Kernelcache image not valid" и
# уходит в recovery. 3 xref к строке @ file 0xa72b2: каждый паттерн
# `bl <hash_check>; cbz w0, <skip_error>`. Заменяем bl на mov w0,#0 →
# skip всегда срабатывает. То же для Device Tree / Ramdisk (если понадобится).
IBOOT_PATCHES = {
    0x7007966c - 0x8: (0x9400547e, MOV_W0_0),  # bl @ file 0xd664 (bl+cbz+error @ 0x7007966c)
    0x70079c7c - 0x8: (0x94005177, MOV_W0_0),  # bl @ file 0xdc74
    0x70079e68 - 0x8: (0x9400500f, MOV_W0_0),  # bl @ file 0xde60
}

IMAGES = [  # order matters: AVPBooter takes the first one (illb); bytes or path
    lambda: patched_im4p(RAW + "LLB.vresearch101.RELEASE.bin", b"illb", LLB_BASE, LLB_PATCHES),
    FW + "all_flash/iBoot.vresearch101.RESEARCH_RELEASE.im4p",
    # session 49 iBoot patches отключены — на нашей сборке ошибка
    # "Kernelcache image not valid" срабатывает через другой код.
    # См. IBOOT_PATCHES выше как reference для будущего.
]


def der_len(n):
    if n < 0x80:
        return bytes([n])
    b = n.to_bytes((n.bit_length() + 7) // 8, "big")
    return bytes([0x80 | len(b)]) + b


def der(tag, body):
    return bytes([tag]) + der_len(len(body)) + body


def patched_im4p(raw, fourcc, base, patches):
    d = bytearray(open(raw, "rb").read())
    for va, (old, new) in patches.items():
        o = va - base
        assert struct.unpack_from("<I", d, o)[0] == old, f"{va:#x}: unexpected insn"
        struct.pack_into("<I", d, o, new)
    # uncompressed IM4P: SEQUENCE { "IM4P", type, description, OCTET STRING payload }
    return der(0x30, der(0x16, b"IM4P") + der(0x16, fourcc) + der(0x16, b"patched") + der(0x04, bytes(d)))


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
        c = img4(p() if callable(p) else open(p, "rb").read())
        assert off + len(c) < 0xa00000, "images overlap NVRAM"
        buf[off:off + len(c)] = c
        print(f"{getattr(p, 'split', lambda _: ['llb(patched)'])('/')[-1]} tag={c[c.find(b'IM4P') + 6:c.find(b'IM4P') + 10]} @ {off:#x} len {len(c):#x}")
        off = (off + len(c) + ALIGN - 1) & -ALIGN
    open(out, "wb").write(buf)
