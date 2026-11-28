#!/usr/bin/env bash
# Start untuk Vercel: migrate + seed (idempotent, pakai advisory lock) ke Postgres eksternal, lalu gunicorn.
set -euo pipefail
: "${DATABASE_URL:?DATABASE_URL belum di-set}"
python deploy/migrate_locked.py
exec gunicorn Inventory_Project.wsgi --bind "0.0.0.0:${PORT:-80}" --workers 2
