import capstone

md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)

f = open('/mnt/d/vphonewin/fw/cloud/raw/dyld.bin', 'rb')

for name, target, off in [("func_824fc", 0x700824fc, 0x824fc), ("func_82338", 0x70082338, 0x82338)]:
    f.seek(off)
    code = f.read(128)
    print(f"\n=======================================================")
    print(f"Disassembly of {name} at {target:#x} (file offset {off:#x}):")
    for ins in md.disasm(code, target):
        print(f"  {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")
