import struct
import capstone

kc_path = "/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin"
with open(kc_path, "rb") as f:
    data = f.read()

text_exec_va = 0xfffffe0007a94000
text_exec_off = 0x00a90000

# Let's inspect all ADRP+ADD instructions between 0xfffffe0007d57400 and 0xfffffe0007d58600
start_va = 0xfffffe0007d57400
end_va   = 0xfffffe0007d58600

start_off = text_exec_off + (start_va - text_exec_va)
end_off   = text_exec_off + (end_va - text_exec_va)

md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)
md.detail = True

def va2data(va):
    # __PRELINK_TEXT: vmaddr=0xfffffe0007008000, fileoff=0x0004000
    if 0xfffffe0007008000 <= va < 0xfffffe0007684000:
        off = 0x4000 + (va - 0xfffffe0007008000)
        s = data[off:off+100].split(b'\0')[0]
        return s.decode('ascii', errors='replace')
    return ""

insns = list(md.disasm(data[start_off:end_off], start_va))
for i, insn in enumerate(insns):
    if insn.mnemonic == 'adrp':
        # check next 1-3 instructions for add
        rd = insn.operands[0].reg
        imm_page = insn.operands[1].imm
        for k in range(1, 4):
            if i + k >= len(insns): break
            next_insn = insns[i+k]
            if next_insn.mnemonic == 'add' and len(next_insn.operands) >= 3:
                if next_insn.operands[1].reg == rd:
                    add_imm = next_insn.operands[2].imm
                    target_va = imm_page + add_imm
                    str_val = va2data(target_va)
                    if str_val:
                        print(f"0x{insn.address:x}: {insn.op_str} -> 0x{target_va:x}: \"{str_val}\"")
                    break
