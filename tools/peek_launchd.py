with open("/home/ard/vrwork/launchd", "rb") as f:
    f.seek(0x4673b)
    print("At 0x4673b:", repr(f.read(64)))
    f.seek(0x46748)
    print("At 0x46748:", repr(f.read(64)))
