import struct, sys

def parse_apfs(path, offset=0):
    print(f"=== Parsing APFS at {path} offset {hex(offset)} ===")
    with open(path, "rb") as f:
        f.seek(offset)
        block0 = f.read(4096)
        magic = block0[32:36]
        print(f"Magic: {magic}")
        if magic != b'NXSB':
            print("Not NXSB!")
            return
        block_size = struct.unpack_from("<I", block0, 36)[0]
        block_count = struct.unpack_from("<Q", block0, 40)[0]
        features = struct.unpack_from("<Q", block0, 48)[0]
        ro_compat = struct.unpack_from("<Q", block0, 56)[0]
        incompat = struct.unpack_from("<Q", block0, 64)[0]
        uuid = block0[72:88].hex()
        next_oid = struct.unpack_from("<Q", block0, 88)[0]
        next_xid = struct.unpack_from("<Q", block0, 96)[0]
        omap_oid = struct.unpack_from("<Q", block0, 160)[0]
        fs_oid_array = []
        for i in range(32):
            oid = struct.unpack_from("<Q", block0, 168 + i*8)[0]
            if oid != 0:
                fs_oid_array.append(oid)
        print(f"block_size={block_size}, block_count={block_count}, uuid={uuid}, fs_oids={fs_oid_array}")

parse_apfs('/home/ard/vrwork/root2.img', 2048 * 512)
parse_apfs('/home/ard/vrwork/root2.img', 64 * 1024 * 1024)
parse_apfs('/mnt/d/vphonewin/_work/rootfs/test-decrypt/094-39278-029.dmg', 0)
