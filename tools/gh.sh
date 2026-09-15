#!/bin/bash
# gh.sh import <name> <file> [raw-base]      — create Ghidra project D:/vphonewin/ghidra/<name> and auto-analyze
# gh.sh dec <name> <out.c> <addr|sym>...     — decompile into out.c (appends)
# gh.sh run <name> <Script.java> [args...]   — run any script from tools/ghidra_scripts
G=/d/vphonewin/tools/ghidra_12.1.3_PUBLIC/support/analyzeHeadless.bat
P=D:/vphonewin/ghidra; mkdir -p /d/vphonewin/ghidra
S=D:/vphonewin/tools/ghidra_scripts
cmd=$1; name=$2; shift 2
case $cmd in
import)
  f=$1; base=$2
  if [ -n "$base" ]; then
    "$G" "$P" "$name" -import "$f" -overwrite -processor AARCH64:LE:64:AppleSilicon -loader BinaryLoader -loader-baseAddr "$base" 2>&1 | grep -E 'ERROR|INFO  (IMPORTING|ANALYZING)|REPORT' | tail -5
  else
    "$G" "$P" "$name" -import "$f" -overwrite 2>&1 | grep -E 'ERROR|IMPORTING|REPORT' | tail -5
  fi ;;
dec)
  out=$1; shift; rm -f "$out"
  "$G" "$P" "$name" -process -noanalysis -scriptPath "$S" -postScript Decomp.java "$out" "$@" 2>&1 | grep -E 'ERROR|Exception' | head -5
  cat "$out" ;;
run)
  scr=$1; shift
  "$G" "$P" "$name" -process -noanalysis -scriptPath "$S" -postScript "$scr" "$@" 2>&1 | grep -E '\.java> |ERROR|Exception|java:[0-9]+: error' | sed -E 's/^INFO +[A-Za-z]+\.java> //; s/ \(GhidraScript\) *$//' ;;
esac
