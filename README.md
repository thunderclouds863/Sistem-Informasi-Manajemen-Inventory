# Sistem Informasi Manajemen Inventory — PT TARINDO

Centralized inventory, purchasing, and warehouse dispatch management system built with **Django** for **PT TARINDO** (*Perusahaan Pengecoran Kuningan — Juwana, Pati, Jawa Tengah*), manufacturer of brass and PVC faucets and sanitary ware (AMICO).

## Key Features

- **Operational Command Center Dashboard**: Real-time counts for Orders, Products, Total Stock, Suppliers, Buyers, Warehouse Drops, Seasons, and Deliveries, paired with an Order Pipeline breakdown and live-filterable Recent Orders table.
- **Role-Based Access Control (RBAC)**:
  - **Administrator (`is_admin` / `is_staff` / `is_superuser`)**: Full CRUD access across Orders (including inline status transitions), Products, Warehouse Drops, Seasons, Suppliers, Buyers, and Deliveries.
  - **Supplier (`is_supplier`)**: Read-only access scoped to their own orders and deliveries, plus catalog visibility.
  - **Buyer (`is_buyer`)**: Read-only access scoped to their own orders and deliveries, plus catalog visibility.
- **Full CRUD & Order Lifecycle**: Create, edit, delete (POST + CSRF + confirmation modal), and transition order statuses (`Pending`, `Approved`, `Processing`, `Complete`, `Bulk`, `Decline`).
- **Account Security**: Split-screen login with password visibility toggle, Remember Me session expiry, inline validation errors, and an authenticated **Account & Password** page (`/users/profile/`).
- **Responsive UI**: Tested across Desktop (`1440×900`), Laptop (`1280×800`), Tablet (`768×1024`), and Mobile (`390×844`) viewports.

## Prerequisites

- Python 3.9+ (tested on Python 3.13 with Django 4.2 and compatible with `requirements.txt`)
- SQLite (bundled with Python)

## Local Setup

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# macOS / Linux:
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Apply database migrations and seed sample data
python manage.py migrate
python manage.py seed_demo

# 4. Run the development server
python manage.py runserver
```

Open `http://127.0.0.1:8000/users/login/` in your browser.

### Demo Accounts (created by `seed_demo`)

| Role | Username | Password |
| :--- | :--- | :--- |
| Administrator | `demo_admin` | `demo123` |
| Supplier | `supplier1` | `demo123` |
| Buyer | `buyer1` | `demo123` |

## Environment Variables

Copy `.env.example` if configuring production/deployment settings:

- `SECRET_KEY`: Django secret key (defaults to a dev-only value locally)
- `DEBUG`: `"True"` or `"False"` (defaults to `"True"`)
- `ALLOWED_HOSTS`: Comma-separated hostnames (e.g. `localhost,127.0.0.1,.onrender.com`)

## Running Tests & Linting

```bash
python manage.py check
python manage.py test
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 . --count --max-complexity=10 --max-line-length=127 --statistics
```
