#!/bin/bash
set -e
Q=~/inferno/build/qemu-system-aarch64
W=~/vrwork
FW=/mnt/d/vphonewin/fw/vz/AVPBooter.vresearch1.bin
TC=/mnt/d/vphonewin/_work/tc/os.trst.bin              # raw `trst` payload for vresearch101 OS DMG

rm -f $W/us.uart $W/us.log $W/kprintf.log $W/svc.log
export VR_NOP="0xfffffe0008ed691c,0xfffffe00088cc774,0xfffffe00088cc788,0xfffffe0007cf3d38,0xfffffe0007cf3d9c,0xfffffe0008f1781c,0xfffffe0008aaab18,0xfffffe0008aaab34"
# 0xfffffe0008ed691c — rootvp auth (release KC: cbnz w0, #0x8ed6b78 panic "rootvp not authenticated").
# 0xfffffe00088cc774,0xfffffe00088cc788 — APFS handle_get_dev_by_role entitlement bypass (Patch 16).
# 0xfffffe0007cf3d38 — AMFI release KC b.ne assertion failed (*cs_flags & initial_cs_flags) NOP.
# 0xfffffe0007cf3d9c — AMFI release KC cbz w0 adhoc rejection check NOP.
# 0xfffffe0008f1781c — bl panic for "exit reason namespace %d subcode 0x%llx" NOP.
#   Prevents kernel panic when critical boot task (mount[3]) exits with error.
#   After NOP, falls through to 0xfffffe0008f17820 which loops back to process next task.
# 0xfffffe0008aaab18 — wfe in AppleSEPBooter SEP wait spin loop (blocks forever without real SEP).
#   NOPing wfe makes execution fall through to the tbz+loop check.
# 0xfffffe0008aaab34 — tbz w8,#4,#0xfffffe0008aaa988 (loop-back branch in SEP wait loop).
#   NOPing this tbz makes execution skip the back-branch and continue forward to cleanup/exit.
export VR_MOV0="0xfffffe0007cf3d6c,0xfffffe00088ce284,0xfffffe00088b779c,0xfffffe0008b06314"
# 0xfffffe0007cf3d6c: mov x0,x21 → mov x0,#0 before retab vnode_check_signature in release KC.
# 0xfffffe00088ce284: APFS handle_fsioc_graft validate_payload_and_manifest -> 0 (Patch 15).
# 0xfffffe00088b779c: APFS mountroot vfs_flags force 0 (RW root mount).
# 0xfffffe0008b06314: vm_fault_enter_prepare bl cs_invalid_page -> mov x0, #0 (allow page validation).
export VR_RET0="0xfffffe00088b8c40,0xfffffe0008ee7e50,0xfffffe0008ab04d4,0xfffffe0008aaa8f0"
# 0xfffffe00088b8c40: APFS apfs_mount_upgrade_checks entry — returns 0 (allow RW remount) (Patch 14).
# 0xfffffe0008ee7e50: cs_invalid_page entry — returns 0 (never kill process on invalid page).
# 0xfffffe0008ab04d4: AppleSEPBooter::_captureiBICKCV entry — returns 0 (no SEP hardware, skip KCV capture).
#   Function has multiple REQUIRE panics (at 0x8ab05dc, 0x8ab0610, 0x8ab064c); VR_RET0 on prologue skips all.
# 0xfffffe0008aaa8f0: AppleSEPBooter SEP wait/send function entry — returns 0 immediately.
#   Contains wfe spin loop at 0x8aaab18 that blocks indefinitely waiting for SEP mailbox event.
#   Without real SEP hardware, wfe never gets a WakeUp Event and the kernel hangs forever.
export VR_B="0xfffffe00088b7e08:0xfffffe00088b8058,0xfffffe0007cf3ce4:0xfffffe0007cf3d90,0xfffffe0007cf3d94:0xfffffe0007cf3dac,0xfffffe0008b06710:0xfffffe0008b06a44,0xfffffe0008ab064c:0xfffffe0008ab05a0,0xfffffe0009271100:0xfffffe00092711e4"
# 0xfffffe00088b7e08:0xfffffe00088b8058 — APFS _apfs_vfsop_mount kernel_task check bypass (Patch 13).
# 0xfffffe0007cf3ce4:0xfffffe0007cf3d90 — AMFI release KC: redirect w24!=0 failure branch directly to success path.
# 0xfffffe0007cf3d94:0xfffffe0007cf3dac — AMFI release KC: force w9=1 and jump directly to flag setting/csblob attach.
# 0xfffffe0008b06710:0xfffffe0008b06a44 — vm_fault_enter_prepare skip os_reason_create(3, 2) directly to exit.
# 0xfffffe0008ab064c:0xfffffe0008ab05a0 — AppleSEPBooter::_captureiBICKCV REQUIRE panic bypass:
#   `bl panic` at 0x8ab064c redirected to the success epilog (mov x0, x19; ldp...; retab) at 0x8ab05a0.
#   Function returns its input pointer (x19) instead of panicking on kIOReturnSuccess != result.
# 0xfffffe0009271100:0xfffffe00092711e4 — kcformat.c _register_kc_type "Invalid KC Kind" bypass:
#   the b.hs at 0x9271100 (fires when arg w0 not in [1..3]) jumped to a panic block; redirect
#   directly to the function's retab epilog at 0x92711e4. Registration for the offending kind
#   is skipped, but the function returns cleanly instead of panicking (caller ignores return).
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
