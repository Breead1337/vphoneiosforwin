import struct, capstone

f = open('/mnt/d/vphonewin/_work/dyld', 'rb')
data = f.read()
md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)

# search for "mrs x..., tpidrro_el0"
# opcode: mrs xt, tpidrro_el0 is 0xd53bd060 | (Rt)
for i in range(0, len(data) - 4, 4):
    word = struct.unpack_from('<I', data, i)[0]
    if (word & 0xffffff00) == 0xd53bd000: # mrs xt, s3_3_c13_c0_3 (tpidrro_el0)
        start = max(0, i - 16)
        chunk = data[start:i+32]
        print(f"\ntpidrro_el0 read at dyld offset {i:#x} (0x{0x70000000+i:08x}):")
        for ins in md.disasm(chunk, i - (i - start)):
            prefix = "==> " if ins.address == i else "    "
            print(f"{prefix}0x{0x70000000+ins.address:08x}: {ins.mnemonic:8s} {ins.op_str}")
