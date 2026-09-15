# pget.py URL START LEN OUT [N] — parallel ranged download of a slice of URL into one file
import sys, threading, urllib.request, os, time
U, S, L, O = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
N = int(sys.argv[5]) if len(sys.argv) > 5 else 16
BLK = 64 << 20
with open(O, 'ab') as f: f.truncate(L)
todo = list(range(0, L, BLK)); lock = threading.Lock(); done = [0]
def worker():
    fd = open(O, 'r+b')
    while True:
        with lock:
            if not todo: return
            off = todo.pop(0)
        end = min(off + BLK, L) - 1
        for t in range(10):
            try:
                r = urllib.request.urlopen(urllib.request.Request(U, headers={'Range': f'bytes={S+off}-{S+end}'}), timeout=60)
                d = r.read()
                if len(d) != end - off + 1: raise IOError('short')
                fd.seek(off); fd.write(d); break
            except Exception as e:
                time.sleep(2)
        else:
            print('FAILED', off, flush=True); os._exit(1)
        with lock: done[0] += len(d)
ts = [threading.Thread(target=worker) for _ in range(N)]
[t.start() for t in ts]
while any(t.is_alive() for t in ts):
    time.sleep(30); print(f'{done[0]>>20}/{L>>20} MB', flush=True)
print('DONE', O, flush=True)
