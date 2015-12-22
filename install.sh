#!/bin/bash

set -e

echo 'deb https://apt.dockerproject.org/repo ubuntu-trusty main' > /etc/apt/sources.list.d/docker.list
apt-get update -qq
apt-get install -y ruby apache2 curl linux-image-extra-$(uname -r)
apt-get install -y docker-engine
a2enmod cgi
rm -f /etc/apache2/sites-enabled/*.conf

cat > /etc/apache2/sites-enabled/buildcurl.conf <<CONFIG
<VirtualHost *:80>
	ScriptAlias /bin/ /opt/buildcurl/bin/

	<Directory /opt/buildcurl/bin/>
		Require all granted
	</Directory>
</VirtualHost>
CONFIG
service apache2 restart
