vals = [3816517011146665824, -1994106544256, 2200267865652, -2129800183808]
for v in vals:
    u = v & 0xffffffffffffffff
    lo = u & 0xffffffff
    hi = (u >> 32) & 0xffffffff
    # signed 32-bit of lo:
    slo = lo if lo < 0x80000000 else lo - 0x100000000
    print(f"v={v} => hex={u:#018x} hi={hi:#010x} lo={lo:#010x} slo={slo}")
