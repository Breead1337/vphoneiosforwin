# list / extract members of a remote zip via HTTP range requests
import sys, zipfile, urllib.request, io
class R(io.RawIOBase):
    def __init__(s,u):
        s.u=u; s.p=0
        s.n=int(urllib.request.urlopen(urllib.request.Request(u,method='HEAD')).headers['Content-Length'])
    def seekable(s): return True
    def readable(s): return True
    def tell(s): return s.p
    def seek(s,o,w=0): s.p={0:o,1:s.p+o,2:s.n+o}[w]; return s.p
    def readinto(s,b):
        if s.p>=s.n: return 0
        e=min(s.p+len(b),s.n)-1
        d=urllib.request.urlopen(urllib.request.Request(s.u,headers={'Range':f'bytes={s.p}-{e}'})).read()
        b[:len(d)]=d; s.p+=len(d); return len(d)
z=zipfile.ZipFile(io.BufferedReader(R(sys.argv[1]),1<<20))
if len(sys.argv)==2:
    for i in z.infolist(): print(i.file_size, i.compress_type, i.filename)
else:
    import re,os
    for i in z.infolist():
        if re.search(sys.argv[2], i.filename):
            out=os.path.join(sys.argv[3], i.filename); os.makedirs(os.path.dirname(out),exist_ok=True)
            with z.open(i) as f, open(out,'wb') as o:
                while (c:=f.read(1<<22)): o.write(c)
            print('ok', out)
