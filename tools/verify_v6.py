#!/usr/bin/env python3
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_LITTLE_ENDIAN
d = open('/home/ard/vrwork/dyld_v6','rb').read()
md = Cs(CS_ARCH_ARM64, CS_MODE_LITTLE_ENDIAN)
print("-- 0x63c94 (should be b 0x51a8) --")
for i in md.disasm(d[0x63c94:0x63c98], 0x63c94):
    print("  0x%x %s %s" % (i.address, i.mnemonic, i.op_str))
print("-- stub @0x51a8 --")
for i in md.disasm(d[0x51a8:0x51c8], 0x51a8):
    print("  0x%x %s %s" % (i.address, i.mnemonic, i.op_str))
print("-- 0x7d98c (should be nop) --")
for i in md.disasm(d[0x7d98c:0x7d990], 0x7d98c):
    print("  0x%x %s %s" % (i.address, i.mnemonic, i.op_str))
