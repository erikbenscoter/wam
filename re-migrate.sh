#!/bin/bash
makemigrations
migrate

makemigrations reservation_manager
makemigrations login
makemigrations monthly_summary
makemigrations owners_point_manager

migrate

py3 manage.py loaddata ./fixtures/*
