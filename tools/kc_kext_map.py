"""Parse Mach-O LC_SEGMENT_64 of raw KC and locate AppleSEPManager kext code."""
import struct, sys

kc_path = '/home/ard/vrwork/kernelcache.release.raw.bin'
with open(kc_path, 'rb') as f:
    kc = f.read()

MH_MAGIC_64 = 0xFEEDFACF
LC_SEGMENT_64 = 0x19

def parse_macho(off):
    magic, cputype, cpusub, filetype, ncmds, sizeofcmds, flags, reserved = struct.unpack_from('<IIIIIIII', kc, off)
    if magic != MH_MAGIC_64:
        return None
    p = off + 32
    segs = []
    for _ in range(ncmds):
        cmd, cmdsize = struct.unpack_from('<II', kc, p)
        if cmd == LC_SEGMENT_64:
            segname = kc[p+8:p+24].rstrip(b'\0').decode(errors='replace')
            vmaddr, vmsize, fileoff, filesize, maxprot, initprot, nsects, sflags = struct.unpack_from('<QQQQIIII', kc, p+24)
            segs.append((segname, vmaddr, vmsize, fileoff, filesize, nsects))
        p += cmdsize
    return ncmds, segs

# Main Mach-O at 0
main = parse_macho(0)
print('=== main KC segments ===')
for s in main[1]:
    print(f"{s[0]:24s} vm=0x{s[1]:x}+0x{s[2]:x} file=0x{s[3]:x}+0x{s[4]:x} nsect={s[5]}")

# Strings we're chasing
str_off = kc.find(b'kIOReturnSuccess == result')
print(f"\nstring 'kIOReturnSuccess == result' file offset = 0x{str_off:x}")
# Which segment covers this offset?
for name, vmaddr, vmsize, fileoff, filesize, ns in main[1]:
    if fileoff <= str_off < fileoff + filesize:
        vmva = vmaddr + (str_off - fileoff)
        print(f"  ↳ in segment {name}, static VA = 0x{vmva:x}")

# Look for AppleSEPManager string / plist
sm_off = kc.find(b'AppleSEPManager')
print(f"\n'AppleSEPManager' first at file offset = 0x{sm_off:x}")
# also find nested kernelcaches: MH_MAGIC_64 at offsets != 0 (prelinked kexts)
print("\n=== Nested MH_MAGIC_64 offsets ===")
p = 0
count = 0
while True:
    p = kc.find(struct.pack('<I', MH_MAGIC_64), p+4)
    if p < 0: break
    count += 1
    if count <= 5:
        info = parse_macho(p)
        if info and info[1]:
            first_text = next((s for s in info[1] if 'TEXT' in s[0]), info[1][0])
            print(f"  @0x{p:x}: first seg {first_text[0]} vm=0x{first_text[1]:x}")
print(f"total nested magics: {count}")
