import struct, capstone, sys
KC="/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin"
f=open(KC,"rb").read(); BASE=0xfffffe0007004000
md=capstone.Cs(capstone.CS_ARCH_ARM64,capstone.CS_MODE_LITTLE_ENDIAN); md.detail=True
va0=int(sys.argv[1],0); n=int(sys.argv[2],0) if len(sys.argv)>2 else 0x60
off=va0-BASE-0x30
for ins in md.disasm(f[off:off+n+0x30], BASE+off):
    mark=">>" if ins.address==va0 else "  "
    print("%s0x%x: %08x  %s %s"%(mark,ins.address,struct.unpack_from("<I",f,ins.address-BASE)[0],ins.mnemonic,ins.op_str))
