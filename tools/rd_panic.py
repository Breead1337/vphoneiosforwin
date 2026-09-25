KC="/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin"
f=open(KC,"rb").read(); BASE=0xfffffe0007004000
# runtime addrs from far=0xe00 dump, slide=0x33184000
slide=0x33184000
for name,rt in [("x1",0xfffffe003a1c73dd),("x2",0xfffffe003a1d8f9a),("x12",0xfffffe003a19207c),("x19_2",0xfffffe003a1d8f9a),("x7_2",0xfffffe003c4429cc)]:
    link=rt-slide; o=link-BASE
    if 0<=o<len(f):
        s=f[o:o+120].split(b"\0")[0]
        print("%-6s link=0x%x: %r"%(name,link,s))
    else:
        print("%-6s link=0x%x: (out of file, runtime-only)"%(name,link))
