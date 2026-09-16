# stage Preboot volume contents the way iBoot fsboot reads them (paths seen via gdb on FUN_700e5770):
#   /active = <96 hex nsih>;  /<nsih>/usr/standalone/firmware/... ; /<nsih>/System/Library/Caches/com.apple.kernelcaches/kernelcache
# usage (WSL): python3 mkpreboot.py outdir
import os, sys
from mkaux import img4

FW = "/mnt/d/vphonewin/fw/cloud/"
NSIH = "0" * 96
FILES = {
    "usr/standalone/firmware/sep-firmware.img4": "Firmware/all_flash/sep-firmware.vresearch101.RELEASE.im4p",
    "usr/standalone/firmware/devicetree.img4": "Firmware/all_flash/DeviceTree.vresearch101ap.im4p",
    "usr/standalone/firmware/root_hash.img4": "Firmware/094-39278-029.dmg.aea.root_hash",
    "usr/standalone/firmware/FUD/StaticTrustCache.img4": "Firmware/094-39278-029.dmg.aea.trustcache",
    "usr/standalone/firmware/FUD/Ap,SecurePageTableMonitor.img4": "Firmware/sptm.vresearch1.release.im4p",
    "usr/standalone/firmware/FUD/Ap,TrustedExecutionMonitor.img4": "Firmware/txm.iphoneos.research.im4p",
    "System/Library/Caches/com.apple.kernelcaches/kernelcache": "kernelcache.research.vresearch101",
}

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
open(os.path.join(out, "active"), "w").write(NSIH)
for dst, src in FILES.items():
    p = os.path.join(out, NSIH, dst)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "wb").write(img4(open(FW + src, "rb").read()))
    print(dst)
