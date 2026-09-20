import struct
import capstone

kc_path = "/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin"
with open(kc_path, "rb") as f:
    data = f.read()

text_exec_va = 0xfffffe0007a94000
text_exec_off = 0x00a90000

start_va = 0xfffffe0007d57400
end_va   = 0xfffffe0007d58600

start_off = text_exec_off + (start_va - text_exec_va)
end_off   = text_exec_off + (end_va - text_exec_va)

md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)

insns = list(md.disasm(data[start_off:end_off], start_va))
print(f"Disassembled {len(insns)} instructions")
for i, insn in enumerate(insns):
    if insn.mnemonic == 'adrp':
        print(f"ADRP at 0x{insn.address:x}: {insn.mnemonic} {insn.op_str}")
        if i + 1 < len(insns):
            print(f"  +1: 0x{insns[i+1].address:x}: {insns[i+1].mnemonic} {insns[i+1].op_str}")
        if i + 2 < len(insns):
            print(f"  +2: 0x{insns[i+2].address:x}: {insns[i+2].mnemonic} {insns[i+2].op_str}")
