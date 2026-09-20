import struct

with open('/home/ard/vrwork/launchd', 'rb') as f:
    hdr = f.read(0x2000)
    ncmds = struct.unpack_from('<I', hdr, 16)[0]
    off = 32
    symtab_off = 0
    nsyms = 0
    str_off = 0
    for _ in range(ncmds):
        cmd, cmdsize = struct.unpack_from('<II', hdr, off)
        if cmd == 2: # LC_SYMTAB
            symoff, nsyms, stroff, strsize = struct.unpack_from('<IIII', hdr, off+8)
            f.seek(symoff)
            symdata = f.read(nsyms * 16)
            f.seek(stroff)
            strdata = f.read(strsize)
            print(f'Found {nsyms} symbols in launchd!')
            # Check symbol names
            for i in range(nsyms):
                n_strx, n_type, n_sect, n_desc, n_value = struct.unpack_from('<IBBHQ', symdata, i*16)
                if n_strx < len(strdata):
                    end = strdata.find(b'\x00', n_strx)
                    sname = strdata[n_strx:end].decode('latin1', errors='replace')
                    if n_value in [0x100058580, 0x1000586c0, 0x100049ae0, 0x100016068] or 'dispatch_main' in sname or 'xpc_main' in sname:
                        print(f'  {hex(n_value)}: {sname}')
        off += cmdsize
