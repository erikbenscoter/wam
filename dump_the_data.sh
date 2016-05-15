#!/bin/bash
python3 manage.py dumpdata login --indent=4 > ./fixtures/login.json
python3 manage.py dumpdata monthly_summary --indent=4 > ./fixtures/monthly_summary.json
python3 manage.py dumpdata owners_point_manager --indent=4 > ./fixtures/owners_point_manager.json
python3 manage.py dumpdata reservation_manager --indent=4 > ./fixtures/reservation_manager.json
