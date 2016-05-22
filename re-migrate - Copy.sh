#!/bin/bash
source /home/erikbenscoter/.bashrc

python3 manage.py migrate

echo "++++ loading fixtures ++++"
python3 manage.py loaddata ./fixtures/*
