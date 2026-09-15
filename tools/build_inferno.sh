#!/bin/bash
# build Inferno-based qemu in WSL: ~/inferno/build/qemu-system-aarch64 (applies D:\vphonewin\overlay first)
set -e
cd ~/inferno
( cd /mnt/d/vphonewin/overlay && find . -type f ) | while read f; do
  mkdir -p "$(dirname "$f")"; sed 's/\r$//' "/mnt/d/vphonewin/overlay/$f" > "$f.tmp"
  if cmp -s "$f.tmp" "$f"; then rm "$f.tmp"; else mv "$f.tmp" "$f"; echo "overlay: $f"; fi
done
mkdir -p build && cd build
[ -f build.ninja ] || ../configure --target-list=aarch64-softmmu --enable-lzfse --enable-slirp --enable-zstd \
  --enable-nettle --enable-gnutls --enable-gtk --enable-sdl --disable-werror --disable-qom-cast-debug --extra-cflags=-Wno-error > ../configure.log 2>&1
nice ninja -j12 qemu-system-aarch64 qemu-img > ../build.log 2>&1 || { grep -A12 "^FAILED" ../build.log | head -60; exit 1; }
ls -la qemu-system-aarch64
