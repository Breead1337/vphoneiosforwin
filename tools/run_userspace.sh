#!/bin/bash
Q=~/inferno/build/qemu-system-aarch64
W=~/vrwork
FW=/mnt/d/vphonewin/fw/vz/AVPBooter.vresearch1.bin

rm -f $W/us.uart $W/us.log
export VR_NOP="0xfffffe0008f3a91c"
export VR_MOV0="0xfffffe0008c19a28"
export VR_B="0xfffffe0008f7b2fc:0xfffffe0008f7adb0,0xfffffe0008f7ad74:0xfffffe0008f7adb0"

timeout ${T:-360} "$Q" -M vresearch101 -smp 1 -m 4G \
  -bios "$FW" \
  -drive if=pflash,format=raw,file="$W/aux.test" \
  -drive if=pflash,format=raw,file="$W/root2.img",file.locking=off \
  -drive if=none,id=root0,format=raw,file="$W/root2.img",file.locking=off \
  -device vmapple-virtio-blk-pci,drive=root0,variant=root \
  -display none -serial file:"$W/us.uart" \
  -d unimp,guest_errors,int -D "$W/us.log" \
  -cpu apple-gxf,pauth-noop=off,pauth-impdef=on

echo "RC=$?"
echo "=== UART tail ==="
tail -n 40 "$W/us.uart"
echo "=== last user panics/exits in log ==="
grep -aE 'udef@x[0-4]=|udef@\*x3\[[0-9]|userspace panic|fsck|launchd|boot task|CS_KILLED|EXIT_REASON' "$W/us.log" | tail -40
echo "=== EL0 fault ring ==="
grep -aE 'el0_ring|EL0 fault|EL0 exception|el0_exception' "$W/us.log" | tail -20
echo "=== exception histogram ==="
grep -aoE 'Taking exception [0-9]+ \[[^]]+\]' "$W/us.log" | sort | uniq -c | sort -rn | head
