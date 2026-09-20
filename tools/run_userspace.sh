#!/bin/bash
set -e
Q=~/inferno/build/qemu-system-aarch64
W=~/vrwork
FW=/mnt/d/vphonewin/fw/vz/AVPBooter.vresearch1.bin
TC=/mnt/d/vphonewin/_work/tc/os.trst.bin              # raw `trst` payload for vresearch101 OS DMG

rm -f $W/us.uart $W/us.log $W/kprintf.log $W/svc.log
export VR_NOP="0xfffffe0008f3a91c,0xfffffe0008f6f214,0xfffffe0008f7c25c,0xfffffe0008c12c5c,0xfffffe0007d5788c,0xfffffe0007d57828,0xfffffe0008ab1540,0xfffffe0008ab15c0,0xfffffe00088cc774,0xfffffe00088cc788"
# 0xfffffe0008f3a91c — rootvp auth (session 35).
# 0xfffffe0008f6f214 — BSD signal psignal(initproc, SIGKILL) bypass (session 48/53).
# 0xfffffe0008f7c25c — reap_child_locked psignal_with_reason(initproc, SIGKILL, BAD_MACHO) bypass (session 53).
# 0xfffffe0008c12c5c — arm_init cbz w8 skips PE_init_platform & pe_serial_init (session 57/58).
# 0xfffffe0007d5788c — AMFI cbz w0 (adhoc check failure) NOP (session 60).
# 0xfffffe0007d57828 — AMFI b.ne assertion failed (*cs_flags & initial_cs_flags) NOP (session 60).
# 0xfffffe0008ab1540 — TXM CodeSignature wrapper b.ne failure path NOP (session 62).
# 0xfffffe0008ab15c0 — TXM CodeSignature selector error b.ne panic NOP (session 62).
# 0xfffffe00088cc774,0xfffffe00088cc788 — APFS handle_get_dev_by_role entitlement bypass (Patch 16).
# Session 49: пробовали NOP на 4 panic (evaluate + BSD signal) — "Kernel
# instruction fetch abort" (unreachable code после noreturn panic).
# Патч kernelcache через tools/patch_kc.py — iBoot отверг ("Kernelcache
# image not valid" через inline hash check не покрытый ADRP-xref).
# Runtime-хуки исчерпаны, дальше нужна пересборка rootfs (см. NOTES 49).
# Session 46 пробовал ещё 2 NOP на shenanigans! panic (0xfffffe000885cfc4/cff0)
# — вернулись к "SIGKILL of init". Root cause — AMFI evaluate детектит
# несоответствие CDHash с TC. Session 47 = реальный CDHash пересчёт.
export VR_MOV0="0xfffffe0008c19a28,0xfffffe0007d5785c,0xfffffe0007d524b0,0xfffffe00088ce284,0xfffffe00088b779c"
# 0xfffffe0008c19a28: PE_init_platform hook (Session 57).
# 0xfffffe0007d5785c: mov x0,x21 → mov x0,#0 before retab vnode_check_signature (Session 52).
# 0xfffffe0007d524b0: mov x0,x24 → mov x0,#0 before retab mpo_proc_check_launch constraints (Session 63).
# 0xfffffe00088ce284: APFS handle_fsioc_graft validate_payload_and_manifest -> 0 (Patch 15).
# 0xfffffe00088b779c: APFS mountroot vfs_flags force 0 (RW root mount).
export VR_RET0="0xfffffe0007eaf750,0xfffffe0007eafb20,0xfffffe0007eb6de8,0xfffffe0007d53c84,0xfffffe00088b8c40"
# 0xfffffe0007eaf750: AppleSEPBooter::_captureiBICKCV() — SEP hardware check early-return (Session 54).
# 0xfffffe0007eafb20: AppleSEPBooter::bootSEP() — SEP boot hardware check early-return (Session 54).
# 0xfffffe0007eb6de8: AppleSEPBooter::checkStatus() — SEP status check panic early-return (Session 54).
# 0xfffffe0007d53c84: StaticPlatformPolicy checkForLaunchWarningsInDaemon entry (pacibsp) — returns 0 (allow) (Session 62).
# 0xfffffe00088b8c40: APFS apfs_mount_upgrade_checks entry — returns 0 (allow RW remount) (Patch 14).
export VR_B="0xfffffe0008f7b2fc:0xfffffe0008f7adb0,0xfffffe0008f7ad74:0xfffffe0008f7adb0,0xfffffe000885cc60:0xfffffe000885cc78,0xfffffe0007d577d4:0xfffffe0007d57880,0xfffffe0007d57a70:0xfffffe0007d57aac,0xfffffe0007d57c58:0xfffffe0007d57c70,0xfffffe0007d57c78:0xfffffe0007d57880,0xfffffe0007d53cb4:0xfffffe0007d53d44,0xfffffe00088b7e08:0xfffffe00088b8058"
# 0xfffffe00088b7e08:0xfffffe00088b8058 — APFS _apfs_vfsop_mount kernel_task check bypass (Patch 13).
# 0xfffffe0007d57a70:0xfffffe0007d57aac — AMFI CT policy (CoreTrust) bypass (Session 62).
# 0xfffffe0007d57c58:0xfffffe0007d57c70 — Skip StaticPlatformPolicy<2> print in vnode_check_signature (Session 63).
# 0xfffffe0007d57c78:0xfffffe0007d57880 — Redirect signature rejection directly to success exit (attaches csblob, w21=0) (Session 63).
# 0xfffffe0007d53cb4:0xfffffe0007d53d44 — StaticPlatformPolicy check bypass in checkForLaunchWarningsInDaemon (Session 62).
# 0xfffffe0007d577d4:0xfffffe0007d57880 — AMFI vnode_check_signature TXM bypass (Session 60).
# Redirects cbz w24 failure branch directly to success path: loads true cs_flags, sets *cs_flags |= 0x20000000,
# attaches csblob, and sets w21 = 0 (allow).
# 0xfffffe000885cc60:0xfffffe000885cc78 — AMFI evaluate.c:0x137b shenanigans! bypass (Session 54).
# b.ne #0xfffffe000885cfc8 (panic) redirected to str xzr,[sp,#0x18] (success return 0).
# AMFI vnode_check_signature @0xfffffe0007d56dd4 — прыжок в начало функции;
# VR_RET0 = "mov x0,#0; ret x30" — MAC hook возвращает 0 (allow) для ЛЮБОГО
# бинаря; позволяет пропатчить fsck (@0x92c stub) не пересчитывая CDHash.
# Найдено xref к строке "AMFI: vnode_check_signature called with platform %d"
# @VA 0xfffffe00071f79e5, ADRP+ADD @0xfffffe0007d56e34, prolog pacibsp @dd4.
# Session 52: убрал VR_RET0 на vnode_check_signature (был 0xfffffe0007d56dd4).
# Вместо него — узкий VR_MOV0 на mov x0,x21 непосредственно перед retab
# @ 0xfffffe0007d5785c. Функция выполнится полностью (out-params правильные),
# но result затрётся в 0 → AMFI allow. Гипотеза: BAD_MACHO SIGKILL init
# был из-за out-params corruption от полного skip функции.
export VR_WATCH="0xfffffe0008f77aac,0xfffffe0008ad5a9c,0xfffffe0008be9f70,0xfffffe0008f99624,0xfffffe0008c704f0,0xfffffe0008f6e7e0,0xfffffe0008fd86f8"
# Session 53: watch func containing "Process 1 exec of %s failed" panic.
# Session 58: 0xfffffe0008ad5a9c — cnputc direct console interception.
# Session 58: 0xfffffe0008be9f70 — kprintf buffer output interception.
# Session 61: 0xfffffe0008f99624 (openat), 0xfffffe0008c704f0 (openat_nocancel)
# Session 61: 0xfffffe0008f6e7e0 (posix_spawn #244), 0xfffffe0008fd86f8 (posix_spawn #544)
export VR_TRUSTCACHE="$TC"                            # QEMU-side pre-load; see overlay/hw/vmapple/vresearch101.c
set +e

timeout ${T:-360} "$Q" -M vresearch101 -smp 1 -m 4G \
  -bios "$FW" \
  -drive if=pflash,format=raw,file="$W/aux.test" \
  -drive if=pflash,format=raw,file="$W/root2.img",file.locking=off \
  -drive if=none,id=root0,format=raw,file="$W/root2.img",file.locking=off \
  -device vmapple-virtio-blk-pci,drive=root0,variant=root \
  -display gtk -serial file:"$W/us.uart" \
  -d unimp,guest_errors,int -D "$W/us.log" \
  -cpu apple-gxf,pauth-noop=off,pauth-impdef=on

echo "RC=$?"
echo "=== UART tail ==="
tail -n 40 "$W/us.uart"
echo "=== kprintf.log tail ==="
if [ -f "$W/kprintf.log" ]; then
  tail -n 80 "$W/kprintf.log"
else
  echo "(kprintf.log is empty or not created)"
fi
echo "=== svc.log tail ==="
if [ -f "$W/svc.log" ]; then
  tail -n 120 "$W/svc.log"
else
  echo "(svc.log is empty or not created)"
fi
echo "=== last user panics/exits in log ==="
grep -aE 'udef@x[0-4]=|udef@\*x3\[[0-9]|userspace panic|fsck|launchd|boot task|CS_KILLED|EXIT_REASON' "$W/us.log" | tail -40
echo "=== EL0 fault ring ==="
grep -aE 'el0_ring|EL0 fault|EL0 exception|el0_exception' "$W/us.log" | tail -20
echo "=== exception histogram ==="
grep -aoE 'Taking exception [0-9]+ \[[^]]+\]' "$W/us.log" | sort | uniq -c | sort -rn | head
