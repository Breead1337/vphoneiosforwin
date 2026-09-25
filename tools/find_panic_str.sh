#!/bin/bash
KC=/mnt/d/vphonewin/fw/cloud/raw/kernelcache.research.vresearch101.bin
for s in 'panic(cpu' 'caller 0x' 'panic: ' 'Debugger called' 'Original panic string' '"@%s:%d' 'assertion failed' 'is not authenticated'; do
  o=$(grep -aboF "$s" "$KC" 2>/dev/null | head -1 | cut -d: -f1)
  [ -n "$o" ] && printf "%-24s file=0x%x va=0x%x\n" "$s" "$o" "$((0xfffffe0007004000+o))"
done
