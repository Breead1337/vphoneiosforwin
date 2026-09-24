#!/usr/bin/env python3
# Locate shared-region function prologues in the research KC (flat map vmaddr=BASE+fileoff).
# Reuses find_roothash_hooks approach: ADRP+ADD xref to each __func__ cstring -> back-scan to pacibsp.
import struct, sys
KC = "/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin"
BASE = 0xfffffe0007004000
data = open(KC, "rb").read()
TEXT_EXEC_FOFF = TEXT_EXEC_SIZE = None
ncmds = struct.unpack_from("<I", data, 16)[0]; p = 32
for _ in range(ncmds):
    cmd, cmdsize = struct.unpack_from("<II", data, p)
    if cmd == 0x19 and data[p+8:p+24].split(b"\0")[0] == b"__TEXT_EXEC":
        vmaddr, vmsize, fileoff, filesize = struct.unpack_from("<QQQQ", data, p+24)
        TEXT_EXEC_FOFF, TEXT_EXEC_SIZE = fileoff, filesize
    p += cmdsize
TEXT_EXEC_VA = BASE + TEXT_EXEC_FOFF
NAMES = [b"vm_shared_region_enter", b"vm_shared_region_get", b"vm_shared_region_lookup",
         b"vm_shared_region_map_file", b"shared_region_map_and_slide_2_np",
         b"shared_region_map_and_slide_np", b"vm_shared_region_by_entitlement",
         b"vm_shared_region_per_team_id", b"vm_shared_region_trim_and_setup",
         b"shared_region_check_np", b"vm_map_enter_mem_object_shr"]
str_va = {}
for nm in NAMES:
    o = data.find(nm + b"\x00")
    if o < 0: o = data.find(nm)
    if o >= 0: str_va[nm.decode()] = BASE + o
    else: print("str", nm.decode(), "NOT FOUND")
targets = set(str_va.values())
code = data[TEXT_EXEC_FOFF:TEXT_EXEC_FOFF+TEXT_EXEC_SIZE]
refs = {va: [] for va in targets}
adrp_page = [None]*32
for a in range(0, len(code)-3, 4):
    w = struct.unpack_from("<I", code, a)[0]
    if (w & 0x9f000000) == 0x90000000:
        rd=w&0x1f; immlo=(w>>29)&3; immhi=(w>>5)&0x7ffff; imm=(immhi<<2)|immlo
        if imm&(1<<20): imm-=(1<<21)
        adrp_page[rd]=((TEXT_EXEC_VA+a)&~0xfff)+(imm<<12)
    elif (w & 0xff800000) == 0x91000000:
        rn=(w>>5)&0x1f; rd=w&0x1f
        if adrp_page[rn] is not None:
            sh=(w>>22)&3; imm12=(w>>10)&0xfff
            val=adrp_page[rn]+(imm12<<(12 if sh==1 else 0))
            if val in refs: refs[val].append(TEXT_EXEC_VA+a)
        if rd!=rn: adrp_page[rd]=None
def pro(ref_pc):
    off=ref_pc-TEXT_EXEC_VA
    for back in range(0,6000,4):
        a=off-back
        if a<0: break
        if struct.unpack_from("<I",code,a)[0]==0xd503237f: return TEXT_EXEC_VA+a
    return None
for lbl,va in str_va.items():
    rs=refs.get(va,[]); pros=[]
    for r in rs:
        p=pro(r)
        if p and p not in pros: pros.append(p)
    print("%-34s refs=%-3d prologues=%s" % (lbl,len(rs),[hex(x) for x in pros[:6]]))
