#!/bin/bash
# pget.sh URL START LEN OUT [N]  — parallel range download of a slice of URL
U=$1; S=$2; L=$3; O=$4; N=${5:-16}
C=$(( (L + N - 1) / N )); pids=()
for i in $(seq 0 $((N-1))); do
  a=$((S + i*C)); e=$((a + C - 1)); [ $e -ge $((S+L-1)) ] && e=$((S+L-1))
  ( for t in 1 2 3 4 5; do curl -sfL --retry 5 -r $a-$e -o "$O.part$i" "$U" && [ $(stat -c %s "$O.part$i") -eq $((e-a+1)) ] && break; done ) & pids+=($!)
done
wait "${pids[@]}"
for i in $(seq 0 $((N-1))); do cat "$O.part$i"; done > "$O" && rm -f "$O".part* && echo DONE $(stat -c %s "$O")
