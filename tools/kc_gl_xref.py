import struct
try: import capstone
except Exception as e: print("no capstone",e); raise SystemExit
KC="/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin"
f=open(KC,"rb").read()
BASE=0xfffffe0007004000
# parse segments/sections to get __TEXT_EXEC __text ranges
segs=[]
off=0
# Mach-O header
magic,cput,cpus,ftype,ncmds,szcmds,flags,res=struct.unpack_from("<IiiIIIII",f,0)
o=32
texts=[]
for i in range(ncmds):
    cmd,csz=struct.unpack_from("<II",f,o)
    if cmd==0x19:
        segname=f[o+8:o+24].split(b"\0")[0].decode()
        vmaddr,vmsize,foff,fsize=struct.unpack_from("<QQQQ",f,o+24)
        nsects=struct.unpack_from("<I",f,o+64)[0]
        so=o+72
        for s in range(nsects):
            sname=f[so:so+16].split(b"\0")[0].decode()
            saddr,ssize=struct.unpack_from("<QQ",f,so+32)
            soff=struct.unpack_from("<I",f,so+48)[0]
            if 'text' in sname or segname=='__TEXT_EXEC':
                texts.append((segname,sname,saddr,ssize,soff))
            so+=80
    o+=csz
# target string VAs
def va_of(fileoff): return BASE+fileoff
targets={va_of(0x241302):"err_init_giga", va_of(0x240ed4):"setGLavail", va_of(0x23cd52):"gl_state_available"}
print("targets:",{hex(k):v for k,v in targets.items()})
md=capstone.Cs(capstone.CS_ARCH_ARM64,capstone.CS_MODE_LITTLE_ENDIAN); md.detail=True
for segname,sname,saddr,ssize,soff in texts:
    code=f[soff:soff+ssize]
    adrp={}
    for ins in md.disasm(code,saddr):
        if ins.mnemonic=="adrp":
            try: adrp[ins.reg_name(ins.operands[0].reg)]=ins.operands[1].imm
            except: pass
        elif ins.mnemonic=="add" and len(ins.operands)==3 and ins.operands[2].type==capstone.arm64.ARM64_OP_IMM:
            try:
                bn=ins.reg_name(ins.operands[1].reg)
                if bn in adrp:
                    va=adrp[bn]+ins.operands[2].imm
                    if va in targets:
                        print("XREF %s at 0x%x (seg %s/%s)"%(targets[va],ins.address,segname,sname))
            except: pass
