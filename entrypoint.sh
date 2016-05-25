#!/bin/bash
set -e
set -o pipefail

test -S /var/run/docker.sock && chown :docker /var/run/docker.sock
if [ ! -f /opt/buildcurl/.env ]; then
	# store required env variables into .env file
	env | grep -f /opt/buildcurl/.env.example > /opt/buildcurl/.env
fi
exec /usr/sbin/apache2ctl "$@"
