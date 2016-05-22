#!/bin/bash
set -e
set -o pipefail

test -S /var/run/docker.sock && chown :docker /var/run/docker.sock
exec /usr/sbin/apache2ctl "$@"
