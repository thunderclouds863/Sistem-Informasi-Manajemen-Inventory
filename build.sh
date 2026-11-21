#!/usr/bin/env bash
# Render build: install, static files, fresh SQLite DB with demo data
set -o errexit
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py seed_demo
