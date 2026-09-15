for h in gitlab.com github.com pypi.org deb.debian.org; do printf "%s " $h; timeout 10 curl -s -o /dev/null -w "%{http_code}\n" https://$h/ || echo FAIL; done
env | grep -i proxy
