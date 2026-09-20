import struct
import capstone

kc_path = "/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin"
with open(kc_path, "rb") as f:
    data = f.read()

text_exec_va = 0xfffffe0007a94000
text_exec_off = 0x00a90000
text_exec_sz = 0x0183c000
s_data = data[text_exec_off:text_exec_off + text_exec_sz]

md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)

# Search for mov x0, #0 (0xd2800000) followed by ret (0xd65f03c0)
target = struct.pack("<II", 0xd2800000, 0xd65f03c0)
idx = 0
found = []
while True:
    idx = s_data.find(target, idx)
    if idx == -1: break
    va = text_exec_va + idx
    found.append(va)
    print(f"Found 'mov x0, #0; ret' at 0x{va:x}")
    idx += 4
    if len(found) >= 5: break
