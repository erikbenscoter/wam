#!/bin/bash
source /home/erikbenscoter/.bashrc

python3 manage.py migrate
#
# echo "++++ initial makemigrations +++++"
# python3 manage.py makemigrations
# python3 manage.py migrate
#
# echo "++++ reservation_manager makemigrations +++++"
# python3 manage.py makemigrations reservation_manager
# python3 manage.py migrate
#
# echo "++++ login/monthly_summary/owners_point_manager makemigrations +++++"
# python3 manage.py makemigrations login
# python3 manage.py makemigrations monthly_summary
# python3 manage.py makemigrations owners_point_manager
#
# echo "++++ migrate ++++"
# python3 manage.py migrate
#
echo "++++ loading fixtures ++++"
python3 manage.py loaddata ./fixtures/*
