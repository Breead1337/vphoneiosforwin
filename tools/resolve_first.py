import re
KC="/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin"
f=open(KC,"rb").read(); BASE=0xfffffe0007004000
E="/home/ard/vrwork/exc.log"
lines=open(E,"rb").read().decode(errors="replace").splitlines()
# find first far=0xe00 block: the [EXC ... far=0xe00] then following lines with vbar/x regs until insn
i=0
while i<len(lines) and 'far=0xe00 ' not in lines[i]: i+=1
block=lines[i:i+12]
print("=== first far=0xe00 block ==="); print("\n".join(block))
# parse vbar
vbar=None; regs={}
for ln in block:
    m=re.search(r'vbar=0x([0-9a-f]+)',ln)
    if m: vbar=int(m.group(1),16)
    for m in re.finditer(r'x(\d+)-\d+ = ([0-9a-f ]+)',ln):
        vals=ln.split('=',1)[1].split()
        base=int(re.search(r'x(\d+)-',ln).group(1))
        for j,v in enumerate(vals):
            try: regs[base+j]=int(v,16)
            except: pass
if vbar:
    slide=vbar-0xfffffe0008a5f000
    print("\nslide=0x%x"%slide)
    for rn in sorted(regs):
        rt=regs[rn]; link=rt-slide; o=link-BASE
        if 0<=o<len(f):
            s=f[o:o+120].split(b"\0")[0]
            if len(s)>=5 and all(0x20<=b<0x7f or b in(9,10) for b in s[:6]):
                print("x%-2d rt=0x%x link=0x%x: %r"%(rn,rt,link,s))
