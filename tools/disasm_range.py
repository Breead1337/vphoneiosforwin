#!/usr/bin/env python3
# Disassemble a vm-address range of a thin arm64e Mach-O, annotating string refs and #8 imms.
import struct, sys
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_LITTLE_ENDIAN
path, start_s, end_s = sys.argv[1], sys.argv[2], sys.argv[3]
start, end = int(start_s, 0), int(end_s, 0)
d = open(path, "rb").read()
ncmds = struct.unpack_from("<I", d, 16)[0]
segs = []; p = 32
for _ in range(ncmds):
    cmd, csize = struct.unpack_from("<II", d, p)
    if cmd == 0x19:
        vmaddr, vmsize, fileoff, filesize = struct.unpack_from("<QQQQ", d, p+24)
        segs.append((vmaddr, vmsize, fileoff, filesize))
    p += csize
def vm_to_foff(vm):
    for vmaddr, vmsize, fileoff, filesize in segs:
        if vmaddr <= vm < vmaddr + filesize:
            return fileoff + (vm - vmaddr)
    return None
def read_cstr(vm):
    fo = vm_to_foff(vm)
    if fo is None: return None
    e = d.find(b"\0", fo)
    s = d[fo:e]
    try: return s.decode("ascii")
    except: return None
fo = vm_to_foff(start)
code = d[fo:fo + (end - start)]
md = Cs(CS_ARCH_ARM64, CS_MODE_LITTLE_ENDIAN); md.detail = False
reg_page = {}
for ins in md.disasm(code, start):
    ann = ""
    m, ops = ins.mnemonic, ins.op_str
    if m == "adrp":
        try:
            rd = ops.split(",")[0].strip()
            page = int(ops.split("#")[1], 0)
            reg_page[rd] = page
        except: pass
    elif m == "add" and "#" in ops:
        parts = [x.strip() for x in ops.split(",")]
        if len(parts) == 3 and parts[1] in reg_page:
            try:
                imm = int(parts[2].replace("#", ""), 0)
                s = read_cstr(reg_page[parts[1]] + imm)
                if s: ann = '  ; "%s"' % s[:48]
            except: pass
    if ("#8" == ops.split(",")[-1].strip()) and m in ("mov", "movz", "orr"):
        ann += "   [#8]"
    if m in ("ret", "retab"): ann += "   [RET]"
    if m in ("bl", "b") and "#" in ops: ann += ""
    print("0x%x: %-8s %s%s" % (ins.address, m, ops, ann))
