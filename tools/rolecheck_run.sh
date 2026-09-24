#!/bin/bash
T=/tmp/t6.apfs
rm -f "$T"; truncate -s 400M "$T"
/home/ard/kbuild/apfsprogs/mkapfs/mkapfs -L Preboot "$T" >/dev/null 2>&1
python3 /mnt/d/vphonewin/tools/role_check.py "$T"
