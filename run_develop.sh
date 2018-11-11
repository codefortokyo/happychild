#!/bin/bash

python manage.py makemigrations
python manage.py migrate

exec gunicorn happychild.wsgi:application -b 0.0.0.0:8000 -w 4
