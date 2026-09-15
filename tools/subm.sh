cd ~/inferno && grep -E 'path' .gitmodules | grep -v roms
for p in $(git config -f .gitmodules --get-regexp path | awk '{print $2}' | grep -v '^roms/'); do git submodule update --init --depth 1 "$p" 2>&1 | tail -1; done
ls util/mlib | head -3
