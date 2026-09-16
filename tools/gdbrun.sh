#!/bin/bash
# run guest under gdbstub and apply a gdb command file: bash gdbrun.sh cmds.gdb   (AUX/ROOT/T as in run1.sh)
Q=~/inferno/build/qemu-system-aarch64
W=~/vrwork
port=$((20000 + RANDOM % 10000))
timeout ${T:-120} $Q -M vresearch101 -smp 1 -m 4G -bios /mnt/d/vphonewin/fw/vz/AVPBooter.vresearch1.bin \
  -drive if=pflash,format=raw,file=$W/${AUX:-aux.img} -drive if=pflash,format=raw,file=$W/${ROOT:-disk.img} \
  -display none -serial file:$W/gdb.uart -gdb tcp::$port -S $EXTRA &
qp=$!
sleep 1
timeout ${T:-120} gdb-multiarch -q -batch -ex "set architecture aarch64" -ex "set pagination off" \
  -ex "target remote :$port" -x "$1" 2>&1 | grep -v '^\[' 
kill $qp 2>/dev/null; wait 2>/dev/null
