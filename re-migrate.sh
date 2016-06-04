#!/bin/bash
source /home/erikbenscoter/.bashrc

echo "+++ makemigrations +++"

python3 manage.py makemigrations reservation_manager
python3 manage.py makemigrations login 
python3 manage.py makemigrations monthly_summary
python3 manage.py makemigrations owners_point_manager
python3 manage.py makemigrations upgrade_recognition

echo "+++ migrate +++"

python3 manage.py migrate

echo "++++ loading fixtures ++++"

python3 manage.py loaddata ./fixtures/*
