#!/bin/sh
python manage.py makemigrations users projects dashboard
python manage.py migrate
python manage.py loaddata 'fixture.json'
python manage.py collectstatic