import struct

def extract():
    im4p = open("/home/ard/vrwork/tc_iphone/043-53486-120.trustcache", "rb").read()
    # Find OCTET STRING (0x04)
    idx = im4p.find(b"\x04\x83\x01\x45\x98")
    if idx == -1:
        # Search generic ASN.1 OCTET STRING
        idx = im4p.find(b"\x04")
    # Actually after IM4P tag 'trst', tag '1', next is OCTET STRING:
    trst_idx = im4p.find(b"trst")
    assert trst_idx != -1
    oct_idx = im4p.find(b"\x04", trst_idx)
    l0 = im4p[oct_idx + 1]
    if l0 & 0x80:
        nbytes = l0 & 0x7f
        length = int.from_bytes(im4p[oct_idx+2 : oct_idx+2+nbytes], "big")
        payload = im4p[oct_idx+2+nbytes : oct_idx+2+nbytes+length]
    else:
        payload = im4p[oct_idx+2 : oct_idx+2+l0]

    ver, uuid, n = struct.unpack_from("<I16sI", payload, 0)
    print(f"iOS TrustCache: ver={ver}, uuid={uuid.hex()}, nentries={n}, payload_len={len(payload)}")
    assert len(payload) == 24 + n * 24
    open("/home/ard/vrwork/tc_iphone/ios_raw.trst.bin", "wb").write(payload)
    print("Extracted to /home/ard/vrwork/tc_iphone/ios_raw.trst.bin successfully!")

if __name__ == "__main__":
    extract()
