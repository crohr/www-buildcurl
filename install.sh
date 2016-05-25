#!/bin/bash

set -e
set -o pipefail

locale-gen en_US.UTF-8
cat > /etc/default/locale <<EOF
LC_ALL=en_US.UTF-8
LANG=en_US.UTF-8
EOF

apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
echo 'deb https://apt.dockerproject.org/repo ubuntu-trusty main' > /etc/apt/sources.list.d/docker.list
echo deb http://apt.newrelic.com/debian/ newrelic non-free > /etc/apt/sources.list.d/newrelic.list
wget -O- https://download.newrelic.com/548C16BF.gpg | apt-key add -
apt-get update -qq
apt-get install -y curl linux-image-extra-$(uname -r) git htop newrelic-sysmond
apt-get install -y docker-engine

mkdir -p /etc/buildcurl
test -f /etc/buildcurl/.env || cat > /etc/buildcurl/.env <<EOF
BUILDCURL_URL=http://$(curl -s ifconfig.co)
$(env | grep "AWS_")
EOF

if [ "$NEWRELIC_KEY" != "" ]; then
	nrsysmond-config --set license_key=$NEWRELIC_KEY
	service newrelic-sysmond restart
fi

docker pull buildcurl/buildcurl
docker run -a stdout --rm --entrypoint /bin/cat buildcurl/buildcurl init/buildcurl.conf > /etc/init/buildcurl.conf
service buildcurl restart
