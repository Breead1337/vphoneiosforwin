T=200 bash /mnt/d/vphonewin/tools/run1.sh >/dev/null 2>&1
echo "sep 0x200 writes: $(grep -c "write 0x200" ~/vrwork/vr.log)"
echo "sep reqs:"; grep -E "sep-mbox: req" ~/vrwork/vr.log
echo "new dev/panic:"; grep -vE "sep-mbox|Backdoor" ~/vrwork/vr.log | grep -iE "unimp|panic|abort|nvme|virtio" | sort -u | head
echo "uart bytes: $(wc -c < ~/vrwork/vr.uart)"
