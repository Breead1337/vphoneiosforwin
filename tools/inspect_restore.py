import zipfile, plistlib

ipsw_path = r"D:\vphonewin\fw\cloudOS_26.4.ipsw"
z = zipfile.ZipFile(ipsw_path)
p = plistlib.loads(z.read("Restore.plist"))

print("SystemRestoreImageFileSystems:", p.get("SystemRestoreImageFileSystems"))
for k, v in p.items():
    if k not in ("DeviceMap", "SystemRestoreImageFileSystems"):
        print(f"{k}: {v}")
