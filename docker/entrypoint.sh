#!/bin/bash
set -eo pipefail
cd /var/www/html && flask db upgrade && python3 server.py --perms
/usr/bin/supervisord -n -c /etc/supervisor/supervisord.conf

exit 0
