"""Migrate + seed demo dengan Postgres advisory lock + fast-path cold start.

Di Vercel beberapa instance container bisa cold-start bersamaan; tanpa lock, `migrate` paralel
bentrok (duplicate pg_type). Lock dipegang lewat koneksi langsung (DATABASE_URL_UNPOOLED) karena
advisory lock sesi tidak andal lewat PgBouncer.

Saat DB sudah pernah di-seed (`_demo_seeded` ada), cold start melewati `migrate` dan `seed_demo`
agar startup container jauh lebih cepat. Pakai `--force` untuk mereset ulang data demo.
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
FORCE = "--force" in sys.argv


def is_seeded(cur):
    cur.execute(
        "SELECT 1 FROM information_schema.tables "
        "WHERE table_schema = 'public' AND table_name = '_demo_seeded'"
    )
    return cur.fetchone() is not None


with connection.cursor() as cur:
    if not FORCE and is_seeded(cur):
        print("Demo DB already seeded; skipping migrate/seed for fast cold start")
        sys.exit(0)
    cur.execute("SELECT pg_advisory_lock(%s)", [LOCK_ID])
try:
    with connection.cursor() as cur:
        if not FORCE and is_seeded(cur):
            print("Demo DB already seeded by another instance")
            sys.exit(0)
    if FORCE:
        call_command("flush", interactive=False, verbosity=1)
    else:
        call_command("migrate", interactive=False, verbosity=1)
    call_command("seed_demo")
    with connection.cursor() as cur:
        cur.execute("CREATE TABLE IF NOT EXISTS _demo_seeded (seeded_at TIMESTAMPTZ DEFAULT NOW())")
        cur.execute("INSERT INTO _demo_seeded DEFAULT VALUES")
finally:
    with connection.cursor() as cur:
        cur.execute("SELECT pg_advisory_unlock(%s)", [LOCK_ID])
