#!/bin/bash
# build linux-apfs-rw (apfs.ko) for the running WSL2 kernel -> ~/kbuild/apfs/apfs.ko ; load: sudo insmod
set -e
KV=$(uname -r | sed 's/-microsoft-standard-WSL2//')
mkdir -p ~/kbuild && cd ~/kbuild
[ -d linux ] || { curl -sL https://github.com/microsoft/WSL2-Linux-Kernel/archive/refs/tags/linux-msft-wsl-$KV.tar.gz | tar xz && mv WSL2-Linux-Kernel-* linux; }
cd linux
[ -f .config ] || { zcat /proc/config.gz > .config; make olddefconfig >/dev/null; }
[ -f Module.symvers ] || nice make -j12 vmlinux modules_prepare > ../kernel.log 2>&1
cd ..; [ -d apfs ] || git clone -q --depth 1 https://github.com/linux-apfs/linux-apfs-rw apfs
cp -n linux/vmlinux.symvers linux/Module.symvers
(cd apfs && ./genver.sh) && make -C linux M=$PWD/apfs modules > apfs.log 2>&1 && ls -la apfs/apfs.ko
