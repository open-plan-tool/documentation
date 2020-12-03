#!/bin/sh
python manage.py makemigrations users projects dashboard
python manage.py migrate
python manage.py loaddata 'benchmarks_fixture.json'
python manage.py collectstatic