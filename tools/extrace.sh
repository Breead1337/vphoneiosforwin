#!/bin/bash
# boot with -d int but keep the log small: first N non-SVC exceptions (with ESR/FAR/ELR) + ELR histogram
# SKIP=regex: also skip those exceptions (e.g. SKIP="Guarded Execution Enter"). usage (WSL): AUX=aux.test ROOT=root.img T=120 bash extrace.sh   -> ~/vrwork/ex.log, uart in vr.uart
Q=~/inferno/build/qemu-system-aarch64
W=~/vrwork
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FW_DIR="${FW_DIR:-$ROOT_DIR/fw}"
timeout ${T:-120} $Q -M vresearch101 -smp 1 -m 4G -bios "${BIOS:-$FW_DIR/vz/AVPBooter.vresearch1.bin}" \
  -drive if=pflash,format=raw,file=$W/${AUX:-aux.img} -drive if=pflash,format=raw,file=$W/${ROOT:-disk.img} \
  -display none -serial file:$W/vr.uart -d int,unimp,guest_errors -D /dev/stdout $EXTRA 2>/dev/null |
awk -v N=${N:-60} '
  /^Taking exception/ { svc = ((ENVIRON["SKIP"] != "" && $0 ~ ENVIRON["SKIP"]) || $0 ~ /\[SVC\]/); if (!svc && shown < N) { blk = 1; shown++ } else blk = 0 }
  /unimplemented|unsupported|sprr|permfault|udef|pacauth|gexit-panic|genter#|^watch |Invalid|invalid|sep-mbox/ { if (u[$0]++ < 3) print }
  blk { print }
  /with ELR/ && !svc { h[$NF]++ }
  END { print "--- ELR histogram (non-SVC)"; for (k in h) print h[k], k }' > $W/ex.log
tail -5 $W/vr.uart
