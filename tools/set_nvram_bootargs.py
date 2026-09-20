import struct

def set_bootargs(img_path, bootargs_str="debug=0x144 -v serial=3"):
    with open(img_path, 'r+b') as f:
        f.seek(0xa00000)
        data = bytearray(f.read(0x80000))
        
        # Check header
        if data[0x20:0x27] != b'\x71\x7b\xfe\x7fcommon':
            print("Warning: unexpected common partition header:", data[0x20:0x30])
        
        # Find where the strings are in common partition (starts at 0x30)
        common_data = data[0x30:]
        
        # Parse existing key=value strings
        strings = []
        pos = 0
        while pos < len(common_data) and common_data[pos] != 0:
            end = common_data.find(b'\0', pos)
            if end == -1:
                break
            strings.append(common_data[pos:end].decode('latin1'))
            pos = end + 1
        
        print(f"Current NVRAM strings ({len(strings)}):")
        for s in strings:
            print("  ", s[:60] + ("..." if len(s) > 60 else ""))
            
        # Update or add boot-args
        new_strings = []
        found = False
        for s in strings:
            if s.startswith("boot-args="):
                new_strings.append(f"boot-args={bootargs_str}")
                found = True
            else:
                new_strings.append(s)
        if not found:
            # Insert boot-args right after auto-boot=true
            idx = 1 if len(new_strings) > 0 and new_strings[0].startswith("auto-boot") else 0
            new_strings.insert(idx, f"boot-args={bootargs_str}")
            
        print("\nNew NVRAM strings:")
        for s in new_strings:
            print("  ", s[:60] + ("..." if len(s) > 60 else ""))
            
        # Rebuild common payload
        payload = bytearray()
        for s in new_strings:
            payload.extend(s.encode('latin1') + b'\0')
            
        # Zero out the rest of the partition up to next partition or end
        # Common partition size is 0x7ffe * 16 = 524,256 bytes
        part_len = 0x7ffe * 16 - 16
        if len(payload) > part_len:
            raise ValueError("Payload exceeds common partition size")
            
        payload.extend(b'\0' * (part_len - len(payload)))
        data[0x30:0x30 + part_len] = payload
        
        f.seek(0xa00000)
        f.write(data)
        print(f"\nSuccessfully wrote {len(bootargs_str)} bytes boot-args to NVRAM in {img_path}")

if __name__ == '__main__':
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else '/home/ard/vrwork/aux.test'
    args = sys.argv[2] if len(sys.argv) > 2 else "debug=0x144 -v serial=3"
    set_bootargs(path, args)
