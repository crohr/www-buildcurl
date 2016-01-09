#!/bin/bash

set -e

apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
echo 'deb https://apt.dockerproject.org/repo ubuntu-trusty main' > /etc/apt/sources.list.d/docker.list
apt-get update -qq
apt-get install -y ruby apache2 curl linux-image-extra-$(uname -r) git htop
apt-get install -y docker-engine
a2enmod cgi
usermod -aG docker www-data

mkdir -p /opt
test -d /opt/buildcurl || git clone https://github.com/crohr/buildcurl.git /opt/buildcurl
chown -R www-data:www-data /opt/buildcurl
mkdir /opt/buildcurl/cache
chmod 2777 /opt/buildcurl/cache

rm -f /etc/apache2/sites-enabled/*.conf

cat > /etc/apache2/sites-enabled/buildcurl.conf <<CONFIG
<VirtualHost *:80>
	ScriptAlias / /opt/buildcurl/cgi-bin/build.cgi

	<Directory /opt/buildcurl/cgi-bin/>
		Require all granted
	</Directory>
</VirtualHost>
CONFIG
service apache2 restart
