import struct

f = r"D:\vphonewin\fw\cloud\raw\LLB.vresearch101.RELEASE.bin"
d = open(f, "rb").read()
base = 0x7006c000

# find "pl011 debug uart reader"
str_pos = d.find(b"pl011 debug uart reader")
print("String offset:", hex(str_pos))
str_addr = base + str_pos
print("String addr:", hex(str_addr))

# find references to this string
for i in range(0, len(d)-8, 8):
    q = struct.unpack('<Q', d[i:i+8])[0]
    if q == str_addr:
        print(f"64-bit pointer at {hex(base+i)}")

# Also search for adrp/add referencing str_addr
for i in range(0, len(d)-8, 4):
    w1, w2 = struct.unpack('<II', d[i:i+8])
    # check adrp + add
    if (w1 & 0x9f000000) == 0x90000000 and (w2 & 0xff800000) == 0x91000000:
        # decode adrp
        immlo = (w1 >> 29) & 3
        immhi = (w1 >> 5) & 0x7ffff
        imm = (immhi << 2) | immlo
        if imm & 0x100000: imm -= 0x200000
        page = ((base + i) & ~0xfff) + (imm << 12)
        # decode add
        shift = (w2 >> 22) & 1
        imm12 = (w2 >> 10) & 0xfff
        if shift: imm12 <<= 12
        target = page + imm12
        if target == str_addr:
            print(f"adrp+add at {hex(base+i)} -> {hex(target)}")
