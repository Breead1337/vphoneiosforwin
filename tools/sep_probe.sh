#!/bin/bash
# Boot vresearch101 and keep the FULL SEP mailbox trace (no dedup) — for XNU AppleSEPBooter opcode discovery.
# usage (from PS via wsl.exe): AUX=aux.test ROOT=root2.img T=420 bash /mnt/d/vphonewin/tools/sep_probe.sh
Q=~/inferno/build/qemu-system-aarch64
W=~/vrwork
: "${T:=300}"
: "${AUX:=aux.test}"
: "${ROOT:=root2.img}"
: "${EXTRA:=-cpu apple-gxf,pauth-noop=off,pauth-impdef=on}"
: "${SEPOUT:=$W/sep.log}"
: "${EXOUT:=$W/sep_ex.log}"
: "${N:=800}"

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FW_DIR="${FW_DIR:-$ROOT_DIR/fw}"

timeout "$T" "$Q" -M vresearch101 -smp 1 -m 4G \
  -bios "${BIOS:-$FW_DIR/vz/AVPBooter.vresearch1.bin}" \
  -drive if=pflash,format=raw,file=$W/$AUX \
  -drive if=pflash,format=raw,file=$W/$ROOT \
  -display none -serial file:$W/vr.uart \
  -d int,unimp,guest_errors -D /dev/stdout $EXTRA 2>/dev/null | \
awk -v N=$N -v EXOUT="$EXOUT" -v SEPOUT="$SEPOUT" '
  BEGIN { shown = 0 }
  /sep-mbox/ { print >> SEPOUT; next }
  /gexit-panic|permfault|udef@|Guarded Execution Exit|VIOLATION|VBAR_EL1/ { print >> EXOUT }
  /^Taking exception/ { svc = ((ENVIRON["SKIP"] != "" && $0 ~ ENVIRON["SKIP"]) || $0 ~ /\[SVC\]/); if (!svc && shown < N) { blk = 1; shown++ } else blk = 0 }
  blk { print >> EXOUT }
'
echo "-- sep.log lines: $(wc -l < $SEPOUT 2>/dev/null || echo 0)"
echo "-- last SEP reqs:"
grep -a 'sep-mbox: req' "$SEPOUT" | tail -80
echo "-- vr.uart tail:"
tail -20 "$W/vr.uart"
