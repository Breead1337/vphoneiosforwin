import subprocess, os

def run():
    subprocess.run(["mkdir", "-p", "/mnt/hyb_inspect"])
    ld = subprocess.check_output(["losetup", "--find", "--show", "-o", "1048576", "/home/ard/vrwork/root2.hybrid.img"]).decode().strip()
    try:
        subprocess.run(["mount", "-t", "apfs", "-o", "ro,vol=1", ld, "/mnt/hyb_inspect"], check=True)
        sb_plist = "/mnt/hyb_inspect/System/Library/LaunchDaemons/com.apple.SpringBoard.plist"
        if os.path.exists(sb_plist):
            print("Found SpringBoard.plist!")
            data = open(sb_plist, "rb").read()
            print(data[:500])
        else:
            print("SpringBoard.plist NOT in LaunchDaemons, searching...")
            for r, d, fs in os.walk("/mnt/hyb_inspect/System/Library/LaunchDaemons"):
                for f in fs:
                    if "springboard" in f.lower():
                        print("Found:", os.path.join(r, f))
        # Also check backboardd
        bb_plist = "/mnt/hyb_inspect/System/Library/LaunchDaemons/com.apple.backboardd.plist"
        print(f"backboardd.plist exists: {os.path.exists(bb_plist)}")
    finally:
        subprocess.run(["umount", "/mnt/hyb_inspect"])
        subprocess.run(["losetup", "-d", ld])

if __name__ == "__main__":
    run()
