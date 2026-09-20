import struct
import capstone

kc_path = "/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin"

with open(kc_path, "rb") as f:
    data = f.read()

text_exec_va = 0xfffffe0007a94000
text_exec_off = 0x00a90000

# Search backwards from 0xfffffe0007d584c0 for pacibsp (0xd503237f)
target_va = 0xfffffe0007d584c0
curr_va = target_va

while curr_va > target_va - 0x1000:
    curr_off = text_exec_off + (curr_va - text_exec_va)
    val = struct.unpack_from("<I", data, curr_off)[0]
    if val == 0xd503237f: # pacibsp
        print(f"Function entry (pacibsp) at 0x{curr_va:x} (offset -0x{target_va - curr_va:x})")
        break
    curr_va -= 4

md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)
entry_off = text_exec_off + (curr_va - text_exec_va)
print(f"\n--- Disassembling function from 0x{curr_va:x} ---")
for insn in md.disasm(data[entry_off:entry_off + 0x150], curr_va):
    print(f"0x{insn.address:x}: {insn.mnemonic:10s} {insn.op_str}")

