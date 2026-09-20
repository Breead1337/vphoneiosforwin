# Let's reverse the checksum algorithm for the 16-byte header
# Header 1: 5a 82 02 00 6e 76 72 61 6d 00 00 00 00 00 00 00
# Header 2: 71 7b fe 7f 63 6f 6d 6d 6f 6e 00 00 00 00 00 00

h1 = bytes.fromhex("5a 82 02 00 6e 76 72 61 6d 00 00 00 00 00 00 00")
h2 = bytes.fromhex("71 7b fe 7f 63 6f 6d 6d 6f 6e 00 00 00 00 00 00")

# Standard CHRP checksum:
# sum = sig; for b in bytes_after_cksum: sum += b; while sum > 0xff: sum = (sum & 0xff) + (sum >> 8); cksum = sum
def chrp_calc(h):
    s = h[0]
    for b in h[2:]:
        s += b
    while s > 0xff:
        s = (s & 0xff) + (s >> 8)
    return s

print(f"h1 chrp_calc: {chrp_calc(h1):#02x}, actual: {h1[1]:#02x}")
print(f"h2 chrp_calc: {chrp_calc(h2):#02x}, actual: {h2[1]:#02x}")

# Try other common checksums:
# 1. sum of all bytes % 256
s1 = (h1[0] + sum(h1[2:])) & 0xff
s2 = (h2[0] + sum(h2[2:])) & 0xff
print(f"h1 sum%256: {s1:#02x}, h2 sum%256: {s2:#02x}")

# 2. 0x100 - sum
print(f"h1 0x100-sum: {(0x100 - s1)&0xff:#02x}, h2 0x100-sum: {(0x100 - s2)&0xff:#02x}")

# 3. xor
x1 = h1[0]
for b in h1[2:]: x1 ^= b
x2 = h2[0]
for b in h2[2:]: x2 ^= b
print(f"h1 xor: {x1:#02x}, h2 xor: {x2:#02x}")
