#!/bin/bash
# w.sh 'any bash' — run a command line in WSL without PowerShell quoting damage: wsl -d Debian -- bash /mnt/d/vphonewin/tools/w.sh "<cmd>"
# (pass the command base64-encoded with -b to dodge quoting completely)
if [ "$1" = "-b" ]; then eval "$(echo "$2" | base64 -d)"; else eval "$*"; fi
