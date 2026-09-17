#!/bin/bash
# boot normally; once UART shows $MARK (default: end of iBoot) switch on QEMU logging ($LOG) via the monitor.
# awk keeps the first $N lines from $START on (RING=k: plus the k lines before it). usage (WSL): AUX=aux.test ROOT=root.img bash latelog.sh -> ~/vrwork/late.log
Q=~/inferno/build/qemu-system-aarch64
W=~/vrwork
mon=/tmp/vrmon.$$; : > $W/vr.uart
timeout ${T:-200} $Q -M vresearch101 -smp 1 -m 4G -bios /mnt/d/vphonewin/fw/vz/AVPBooter.vresearch1.bin \
  -drive if=pflash,format=raw,file=$W/${AUX:-aux.img} -drive if=pflash,format=raw,file=$W/${ROOT:-disk.img} \
  -display none -serial file:$W/vr.uart -monitor unix:$mon,server,nowait -D /dev/stdout $EXTRA 2>/dev/null |
  awk -v N=${N:-4000} -v S="${START:-.}" -v R=${RING:-0} '
    R && !on { buf[i++ % R] = $0 }
    $0 ~ S && !on { on = 1; if (R) for (k = i > R ? i - R : 0; k < i; k++) print buf[k % R] }
    on && n < N { print; n++ }' > $W/late.log &
until grep -q "${MARK:-End of iBoot}" $W/vr.uart 2>/dev/null; do sleep 0.2; done
python3 -c "import socket,sys,time; s=socket.socket(socket.AF_UNIX); s.connect('$mon'); time.sleep(0.2); s.send(b'log ${LOG:-int,exec,nochain,cpu}\n'); time.sleep(0.5)"
wait
wc -l $W/late.log
