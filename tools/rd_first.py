KC="/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin"
f=open(KC,"rb").read(); BASE=0xfffffe0007004000; slide=0x33184000
# FIRST far=0xe00 dump registers (initial panic-handler entry)
regs={"x19":0xfffffe003a7b8920,"x21":0xfffffe003baa1a58,"x25":0xfffffe003c740000,
      "x26":0xfffffe1e3de629b0,"x27":0xfffffe001a188000,"x28":0xfffffe001a2a4000,
      "x12":0xfffffe003a19207c,"x16strip":0x2badfe250c147430&0xffffffffff}
for n,rt in regs.items():
    link=rt-slide; o=link-BASE
    if 0<=o<len(f):
        s=f[o:o+140].split(b"\0")[0]
        printable=all(0x20<=b<0x7f or b in (9,10) for b in s[:8]) if s else False
        print("%-9s link=0x%x off=0x%x: %s"%(n,link,o, repr(s) if printable and len(s)>=4 else "(nonstr) bytes=%s"%f[o:o+16].hex()))
    else:
        print("%-9s link=0x%x: (out of KC file, runtime memory)"%(n,link))
