with open('/home/ard/vrwork/aux.test', 'rb') as f:
    f.seek(0xa00000)
    data = f.read(512)
    # Print hex dump
    for i in range(0, len(data), 16):
        chunk = data[i:i+16]
        hex_str = ' '.join(f'{b:02x}' for b in chunk)
        ascii_str = ''.join(chr(b) if 0x20 <= b < 0x7f else '.' for b in chunk)
        print(f'{i:04x}: {hex_str:<48}  {ascii_str}')
