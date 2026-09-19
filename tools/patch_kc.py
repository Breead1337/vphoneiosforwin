# patch_kc.py OUT.im4p — kernelcache with _captureiBICKCV bl calls NOP'd.
# XNU asks SEPROM for the iBIC KCV; on vresearch101 our SEP-mbox stub doesn't answer that flow, so XNU panics
# with "REQUIRE fail: kIOReturnSuccess == result" in AppleSEPBooter::_captureiBICKCV. Two callers -> NOP them
# and the KCV bytes stay 0, which the code path tolerates (it just fills a KCV buffer, no downstream check breaks
# until we get further and can implement the SEP protocol properly).
import struct, sys
from mkaux import der

RAW = __file__.rsplit("tools", 1)[0] + "fw/cloud/raw/kernelcache.research.vresearch101.bin"
NOP = 0xd503201f
PATCHES = {  # VA -> (expected_word, new_word)
    0xfffffe0007eafd10: (0x97fffe90, NOP),  # bl _captureiBICKCV (first caller, delta=-0x5c0)
    0xfffffe0007eafd50: (0x97fffe80, NOP),  # bl _captureiBICKCV (second caller, delta=-0x600)
    # Session 49 — AMFI evaluate.c "shenanigans!" + BSD SIGKILL-init panics.
    # Оба — исходы одного AMFI-детектора (session 48 замкнутый круг). NOP на
    # bl panic() → panic не вызывается, следующая инструкция валидна.
    0xfffffe000885cfc4: (0x942950c9, NOP),  # bl panic("shenanigans!" @evaluate.c:0x137b)
    0xfffffe000885cff0: (0x942950be, NOP),  # bl panic("shenanigans!" evaluate.c 2nd)
    0xfffffe0008f6f214: (0x9400b9a4, NOP),  # bl panic("SIGKILL of init"), BSD signal caller 1
    0xfffffe0008f6f400: (0x9400b929, NOP),  # bl panic("SIGKILL of init"), caller 2
}


def va_to_fo(d, va):
    ncmds = struct.unpack_from("<I", d, 16)[0]; o = 32
    for _ in range(ncmds):
        cmd, sz = struct.unpack_from("<II", d, o)
        if cmd == 0x19:
            vm, vs, fo, fs = struct.unpack_from("<QQQQ", d, o + 24)
            if vm <= va < vm + fs:
                return fo + va - vm
        o += sz
    raise SystemExit(f"{va:#x} not mapped")


d = bytearray(open(RAW, "rb").read())
for va, (old, new) in PATCHES.items():
    fo = va_to_fo(d, va)
    have = struct.unpack_from("<I", d, fo)[0]
    assert have == old, f"{va:#x}@fo={fo:#x}: have {have:#x} want {old:#x}"
    struct.pack_into("<I", d, fo, new)
    print(f"patch {va:#x} (fo={fo:#x}): {old:#010x} -> {new:#010x}")

tmp = sys.argv[1] + ".raw"
open(tmp, "wb").write(bytes(d))
import os, subprocess
tools = os.path.dirname(os.path.abspath(__file__))
subprocess.check_call([os.path.join(tools, "ipsw.exe"), "img4", "im4p", "create",
                       "--type", "krnl", "--version", "patched", "--compress", "lzfse_iboot",
                       "--output", sys.argv[1], tmp])
os.remove(tmp)
print(f"wrote {sys.argv[1]}: {len(d):#x} raw -> {os.path.getsize(sys.argv[1]):#x} compressed IM4P")
