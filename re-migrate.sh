#!/bin/bash

echo "+++ makemigrations +++"

python3 manage.py makemigrations django.contrib.admin
python3 manage.py makemigrations django.contrib.auth
python3 manage.py makemigrations django.contrib.contenttypes
python3 manage.py makemigrations django.contrib.sessions
python3 manage.py makemigrations django.contrib.messages
python3 manage.py makemigrations django.contrib.staticfiles
python3 manage.py makemigrations reservation_manager
python3 manage.py makemigrations monthly_summary
python3 manage.py makemigrations login
python3 manage.py makemigrations owners_point_manager
python3 manage.py makemigrations upgrade_recognition
python3 manage.py makemigrations guest_reservation_manager

echo "+++ migrate +++"

python3 manage.py migrate

echo "++++ loading fixtures ++++"

python3 manage.py loaddata ./fixtures/*
