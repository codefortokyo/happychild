#!/bin/bash

python manage.py collectstatic --clear --noinput
python manage.py collectstatic --noinput
python manage.py migrate

exec gunicorn happy_child.wsgi:application -b 0.0.0.0:8000 -w 4
