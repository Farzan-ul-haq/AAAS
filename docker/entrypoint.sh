#!/bin/bash
python3 manage.py migrate && python3 manage.py collectstatic --noinput
# cp -rf staticfiles/* static/
# exec /usr/bin/supervisord
python3 manage.py runserver 0.0.0.0:80
# /usr/local/bin/docker-entrypoint.sh unitd --no-daemon --control unix:/var/run/control.unit.sock
