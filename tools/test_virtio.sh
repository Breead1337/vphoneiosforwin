#!/bin/bash
Q=~/inferno/build/qemu-system-aarch64
W=~/vrwork
FW=/mnt/d/vphonewin/fw/vz/AVPBooter.vresearch1.bin

echo "Testing QEMU with BOTH bdif root AND vmapple-virtio-blk-pci..."
timeout 60 "$Q" -M vresearch101 -smp 1 -m 4G \
  -bios "$FW" \
  -drive if=pflash,format=raw,file="$W/aux.test" \
  -drive if=pflash,format=raw,file="$W/root2.img",file.locking=off \
  -drive if=none,id=root0,format=raw,file="$W/root2.img",file.locking=off \
  -device vmapple-virtio-blk-pci,drive=root0,variant=root \
  -display none -serial file:"$W/vr_vblk.uart" \
  -d unimp,guest_errors -D "$W/vr_vblk.log" \
  -cpu apple-gxf,pauth-noop=off,pauth-impdef=on

echo "RC=$?"
echo "=== UART ==="
tail -n 40 "$W/vr_vblk.uart"
echo "=== UNIMP / PCI LOG ==="
grep -iE "vmapple|virtio|pci|bdif|root" "$W/vr_vblk.log" | head -n 40
