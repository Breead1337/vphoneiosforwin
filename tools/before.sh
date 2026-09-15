# before.sh PATTERN [N] — show the N trace TBs preceding the first log line matching PATTERN
f=~/vrwork/vr.log; n=$(grep -n -m1 -- "$1" $f | cut -d: -f1); [ -z "$n" ] && { echo "no match"; exit; }; sed -n "${n}p" $f
head -n $n $f | grep -E 'Trace|sep-mbox|Taking|bdif' | tail -n ${2:-40} | sed -E 's/Trace [0-9]+: 0x[0-9a-f]+ \[[0-9a-f]+\/0*([0-9a-f]+)\/.*/TB \1/'
