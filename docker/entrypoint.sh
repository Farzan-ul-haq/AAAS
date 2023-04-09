#!/bin/bash
python3 manage.py migrate && python3 manage.py collectstatic --noinput
# cp -rf staticfiles/* static/
exec /usr/bin/supervisord
# /usr/local/bin/docker-entrypoint.sh unitd --no-daemon --control unix:/var/run/control.unit.sock
