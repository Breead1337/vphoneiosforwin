import sys
def der_len(n):
    if n < 0x80: return bytes([n])
    b = n.to_bytes((n.bit_length()+7)//8, "big")
    return bytes([0x80|len(b)]) + b
def im4p(fourcc, payload, desc=b"1"):
    body = b"\x16\x04IM4P" + b"\x16\x04"+fourcc + b"\x16"+bytes([len(desc)])+desc + b"\x04"+der_len(len(payload))+payload
    return b"\x30"+der_len(len(body))+body
def img4(im4p_body):
    body = b"\x16\x04IMG4" + im4p_body
    return b"\x30"+der_len(len(body))+body
src = sys.argv[1] if len(sys.argv)>1 else "/mnt/d/vphonewin/_work/tc/merged.trst.bin"
out = sys.argv[2] if len(sys.argv)>2 else "/home/ard/vrwork/new_static_tc.img4"
payload = open(src,"rb").read()
data = img4(im4p(b"trst", payload))
open(out,"wb").write(data)
print("built %s: %d bytes (payload %d) first32=%s" % (out, len(data), len(payload), data[:32].hex()))
# sanity: re-parse
for tag in [b"IMG4",b"IM4P",b"trst"]:
    print("  ",tag.decode(),"@",hex(data.find(tag)))
