#!/usr/bin/env bash
# Start untuk Vercel: migrate + seed (idempotent) ke Postgres eksternal, lalu gunicorn.
set -euo pipefail
: "${DATABASE_URL:?DATABASE_URL belum di-set}"
python manage.py migrate --no-input
python manage.py seed_demo
exec gunicorn Inventory_Project.wsgi --bind "0.0.0.0:${PORT:-80}" --workers 2
