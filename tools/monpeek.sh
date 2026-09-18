#!/bin/bash
# boot, wait T seconds, stop the VM and run monitor commands from $CMDS (';'-separated, "PC" is replaced by the current pc)
# usage (WSL): AUX=aux.test ROOT=root.img T=100 CMDS='x /4wx PC;gva2gpa PC' bash monpeek.sh -> stdout
Q=~/inferno/build/qemu-system-aarch64
W=~/vrwork
mon=/tmp/vrmon.$$
$Q -M vresearch101 -smp 1 -m 4G -bios /mnt/d/vphonewin/fw/vz/AVPBooter.vresearch1.bin \
  -drive if=pflash,format=raw,file=$W/${AUX:-aux.img} -drive if=pflash,format=raw,file=$W/${ROOT:-disk.img} \
  -display none -serial file:$W/vr.uart -monitor unix:$mon,server,nowait $EXTRA 2>$W/peek.err &
qp=$!
sleep ${T:-100}
python3 - "$mon" "$CMDS" <<'EOF'
import socket, sys, time, re
s = socket.socket(socket.AF_UNIX); s.connect(sys.argv[1]); s.settimeout(3)
def cmd(c):
    s.send(c.encode() + b'\n'); time.sleep(0.4); out = b''
    try:
        while (b := s.recv(65536)): out += b
    except socket.timeout: pass
    return re.sub(r'\x1b\[[0-9;]*[A-Za-z]', '', out.decode(errors='replace'))
cmd('stop')
regs = cmd('info registers'); print(regs)
pc = re.search(r'PC=([0-9a-f]+)', regs).group(1)
for c in sys.argv[2].split(';'):
    c = c.replace('PC', '0x' + pc); print('>>', c); print(cmd(c))
cmd('quit')
EOF
kill $qp 2>/dev/null
