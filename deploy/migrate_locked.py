"""Migrate + seed demo dengan Postgres advisory lock.

Di Vercel beberapa instance container bisa cold-start bersamaan; tanpa lock, `migrate` paralel
bentrok (duplicate pg_type). Lock dipegang lewat koneksi langsung (DATABASE_URL_UNPOOLED) karena
advisory lock sesi tidak andal lewat PgBouncer.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import django

if os.environ.get("DATABASE_URL_UNPOOLED"):
    os.environ["DATABASE_URL"] = os.environ["DATABASE_URL_UNPOOLED"]
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Inventory_Project.settings")
django.setup()

from django.core.management import call_command  # noqa: E402
from django.db import connection  # noqa: E402

LOCK_ID = 7350001
with connection.cursor() as cur:
    cur.execute("SELECT pg_advisory_lock(%s)", [LOCK_ID])
try:
    call_command("migrate", interactive=False, verbosity=1)
    call_command("seed_demo")
finally:
    with connection.cursor() as cur:
        cur.execute("SELECT pg_advisory_unlock(%s)", [LOCK_ID])
