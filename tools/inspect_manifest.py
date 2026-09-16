import zipfile, plistlib

ipsw_path = r"D:\vphonewin\fw\cloudOS_26.4.ipsw"
z = zipfile.ZipFile(ipsw_path)
data = z.read("BuildManifest.plist")
p = plistlib.loads(data)

identities = p.get("BuildIdentities", [])
print(f"Total build identities: {len(identities)}")

for idx, b in enumerate(identities):
    info = b.get("Info", {})
    dev = info.get("DeviceClass")
    manifest = b.get("Manifest", {})
    if "vresearch101" in str(dev) or any("vresearch101" in str(v.get("Info", {}).get("Path", "")) for v in manifest.values()):
        print(f"\n=== Identity {idx}: DeviceClass={dev} ===")
        for comp_name, comp_info in manifest.items():
            path = comp_info.get("Info", {}).get("Path", "")
            is_fw = comp_info.get("Info", {}).get("IsFirmwarePayload", False)
            print(f"  {comp_name:25}: {path}")
