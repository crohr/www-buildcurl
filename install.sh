#!/bin/bash

set -e

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
apt-get install -y ruby apache2 curl linux-image-extra-$(uname -r) git htop newrelic-sysmond
apt-get install -y docker-engine
a2enmod cgi
usermod -aG docker www-data
gem install aws-sdk dotenv --no-ri --no-rdoc

mkdir -p /opt
test -d /opt/buildcurl || git clone https://github.com/crohr/buildcurl.git /opt/buildcurl
chown -R www-data:www-data /opt/buildcurl
mkdir -p /opt/buildcurl/cache
chmod 2777 /opt/buildcurl/cache

test -f /opt/buildcurl/.env || cat > /opt/buildcurl/.env <<EOF
BUILDCURL_URL=http://$(curl -s ifconfig.co)
$(env | grep "AWS_")
EOF

rm -f /etc/apache2/sites-enabled/*.conf

cp /opt/buildcurl/conf/buildcurl.conf /etc/apache2/sites-enabled/

service apache2 restart

if [ "$NEWRELIC_KEY" != "" ]; then
	nrsysmond-config --set license_key=$NEWRELIC_KEY
	service newrelic-sysmond restart
fi
