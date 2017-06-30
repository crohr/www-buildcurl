#!/bin/bash
set -e

if ! gem list -i dotenv -v 2.2.1 ; then
	gem install dotenv -v 2.2.1 --no-ri --no-rdoc
fi

$APP_NAME config:set AUTOUPGRADE=true

a2dissite 000-default
cp -f $APP_HOME/conf/buildcurl.conf /etc/apache2/sites-enabled/buildcurl.conf
systemctl reload apache2
