#!/usr/bin/env bash

python manage.py collectstatic --clear --noinput
python manage.py collectstatic --noinput

exec gunicorn happy_child.wsgi:application -b 0.0.0.0:8000 -w 4
