import subprocess, os

def run():
    subprocess.run(["mkdir", "-p", "/mnt/hyb_inspect"])
    ld = subprocess.check_output(["losetup", "--find", "--show", "-o", "1048576", "/home/ard/vrwork/root2.hybrid.img"]).decode().strip()
    try:
        subprocess.run(["mount", "-t", "apfs", "-o", "ro,vol=1", ld, "/mnt/hyb_inspect"], check=True)
        print("=== /sbin ===")
        print(os.listdir("/mnt/hyb_inspect/sbin"))
        print("\n=== /usr/libexec/backboardd ===")
        print(os.path.exists("/mnt/hyb_inspect/usr/libexec/backboardd"))
        print("\n=== /bin ===")
        print(os.listdir("/mnt/hyb_inspect/bin"))
    finally:
        subprocess.run(["umount", "/mnt/hyb_inspect"])
        subprocess.run(["losetup", "-d", ld])

if __name__ == "__main__":
    run()
