# run AVPBooter on vresearch101 for N seconds, log to $HOME/vrwork/vr.log
Q=~/inferno/build/qemu-system-aarch64
W=~/vrwork; mkdir -p $W
[ -f $W/aux.img ] || truncate -s 128M $W/aux.img
[ -f $W/disk.img ] || truncate -s 64G $W/disk.img
timeout ${T:-20} $Q -M vresearch101 -smp 1 -m 4G -bios /mnt/d/vphonewin/fw/vz/AVPBooter.vresearch1.bin \
  -drive if=pflash,format=raw,file=$W/aux.img -drive if=pflash,format=raw,file=$W/disk.img \
  -display none -serial file:$HOME/vrwork/vr.uart -d unimp,guest_errors${D} -D $HOME/vrwork/vr.log $EXTRA
echo "rc=$?"; echo "--- uart"; cat $HOME/vrwork/vr.uart | head -${N:-80}; echo "--- log"; sort $HOME/vrwork/vr.log | uniq -c | sort -rn | head -${N:-60}
