# PU Document Sewa

Server-rendered Django application for applying to Pokhara University documents
(transcripts, certificates, etc.) online, with staff review and delivery tracking.

Replaces the original NestJS/Prisma API with a single Django project.

## Stack

- Django 6 (session auth, server-rendered templates, Tailwind via CDN)
- PostgreSQL
- Python 3.14

## Apps

| App | Purpose |
|---|---|
| `accounts` | Custom user model (email login, roles: Student / Admin / College Staff), register/login/profile |
| `colleges` | College directory |
| `catalog` | Document-type catalog with fees and required documents |
| `applications` | Application workflow (submit, upload files, staff review, status updates) |

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env   # then edit DB credentials / SECRET_KEY

python manage.py migrate
python manage.py seed   # optional: 3 colleges, 6 document types, admin user
python manage.py runserver
```

App: http://localhost:8000/
Django admin: http://localhost:8000/admin/

Seeded admin login: `admin@pu.edu.np` / `Admin123!` (change it after first login).

## Environment variables (`.env`)

| Var | Description |
|---|---|
| `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` | PostgreSQL connection |
| `DEBUG` | `True`/`False` |
| `ALLOWED_HOSTS` | Comma-separated hostnames |
| `SECRET_KEY` | Django secret key |

## Main URLs

- `/` — document catalog
- `/documents/<slug>/` — document detail
- `/colleges/` — college directory
- `/accounts/register|login|logout|profile/`
- `/applications/apply/` — new application (file upload)
- `/applications/mine/` — student's applications
- `/applications/admin/` — staff dashboard (role: ADMIN / COLLEGE_STAFF)
- `/admin/` — Django admin
