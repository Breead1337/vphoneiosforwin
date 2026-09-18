#!/usr/bin/env python3
"""
unslide.py — Translate slid runtime kernel addresses back to static unslid VAs.

Usage:
  python3 unslide.py <slid_addr> [<slid_addr2> ...] [--slide 0x...] [--log path/to/vr.log] [--kc path/to/kernelcache]

Examples:
  python3 unslide.py 0xfffffe004bb85340 --slide 0x44000000
  python3 unslide.py 0xfffffe004bb85340 --log ~/vrwork/vr.log
"""

import argparse
import os
import re
import struct
import sys

STATIC_VBAR = 0xfffffe0008a5f000
STATIC_PANIC_CSTRING = 0xfffffe00070433dd


def find_slide_from_log(log_path):
    if not os.path.exists(log_path):
        return None
    with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # Pattern 1: sptm slide=0x...
    m = re.search(r"sptm slide=(0x[0-9a-fA-F]+)", content)
    if m:
        return int(m.group(1), 16)

    # Pattern 2: VBAR_EL1 / vbar=0x...
    m = re.search(r"vbar(?:_el1)?[:=\s]+(0x[0-9a-fA-F]+)", content, re.IGNORECASE)
    if m:
        vbar = int(m.group(1), 16)
        if vbar >= 0xfffffe0000000000:
            return vbar - STATIC_VBAR

    # Pattern 3: udef panic cstring pointer vs static
    m = re.search(r'udef@x1="(?:0x)?([0-9a-fA-F]+)"\s+.*panic', content)
    if m:
        slid_panic = int(m.group(1), 16)
        if slid_panic > STATIC_PANIC_CSTRING:
            return slid_panic - STATIC_PANIC_CSTRING

    return None


def va_to_file_offset(kc_path, va):
    if not os.path.exists(kc_path):
        return None
    with open(kc_path, "rb") as f:
        header = f.read(32)
        if len(header) < 32:
            return None
        ncmds, sizeofcmds = struct.unpack_from("<II", header, 16)
        header += f.read(sizeofcmds)  # fileset kernelcaches have far more than 4K of load commands
        o = 32
        for _ in range(ncmds):
            if o + 8 > len(header):
                break
            cmd, sz = struct.unpack_from("<II", header, o)
            if cmd == 0x19:  # LC_SEGMENT_64
                vm, vs, fo, fs = struct.unpack_from("<QQQQ", header, o + 24)
                if vm <= va < vm + fs:
                    return fo + (va - vm)
            o += sz
    return None


def main():
    parser = argparse.ArgumentParser(description="KASLR unslide helper for vresearch101 XNU kernel")
    parser.add_argument("addresses", nargs="+", help="One or more slid virtual addresses (e.g. 0xfffffe004bb85340)")
    parser.add_argument("-s", "--slide", help="KASLR slide in hex (e.g. 0x44000000)")
    parser.add_argument("-l", "--log", help="Path to QEMU log file to extract slide from (default: ~/vrwork/vr.log)")
    parser.add_argument("-k", "--kc", help="Path to raw kernelcache Mach-O binary (for file offset calculation)")

    args = parser.parse_args()

    slide = None
    if args.slide:
        slide = int(args.slide, 0)
    else:
        log_candidates = [
            args.log,
            os.path.expanduser("~/vrwork/vr.log"),
            os.path.expanduser("~/vrwork/ex.log"),
            "vr.log",
            "ex.log",
        ]
        for candidate in log_candidates:
            if candidate and os.path.exists(candidate):
                slide = find_slide_from_log(candidate)
                if slide is not None:
                    print(f"[*] Detected KASLR slide from {candidate}: {slide:#010x}")
                    break

    if slide is None:
        print("[!] Warning: KASLR slide could not be auto-detected from log. Provide --slide 0x... manually.", file=sys.stderr)
        slide = 0

    kc_candidates = [
        args.kc,
        os.path.join(os.path.dirname(__file__), "../fw/cloud/raw/kernelcache.research.vresearch101.bin"),
        os.path.join(os.path.dirname(__file__), "../fw/cloud/kernelcache.research.vresearch101"),
    ]
    kc_path = next((p for p in kc_candidates if p and os.path.exists(p)), None)

    print("-" * 78)
    for raw_addr in args.addresses:
        try:
            slid_va = int(raw_addr, 0)
        except ValueError:
            print(f"[!] Invalid address: {raw_addr}")
            continue

        unslid_va = slid_va - slide
        fo = va_to_file_offset(kc_path, unslid_va) if kc_path else None

        print(f"Slid VA:       {slid_va:#018x}")
        print(f"Slide:         {slide:#010x}")
        print(f"Unslid VA:     {unslid_va:#018x}")
        if fo is not None:
            print(f"File Offset:   {fo:#010x} in {os.path.basename(kc_path)}")
        print(f"Hook syntax:   {unslid_va:#018x} (for VR_MOV0 / VR_RET0 / VR_WATCH)")
        print(f"ipsw disass:   ipsw macho disass -a {unslid_va:#x} -c 20 -q")
        print(f"ipsw a2o:      ipsw macho a2o {unslid_va:#x}")
        print("-" * 78)


if __name__ == "__main__":
    main()
