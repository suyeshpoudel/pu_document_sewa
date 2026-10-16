# PU Document Sewa

Delivery desk for Pokhara University documents (transcripts, certificates, etc.).

Students apply and pay the **PU fee** on the official PU portal
(**[services.pu.edu.np](https://services.pu.edu.np)**) — for a single certificate or
the **TMP bundle** (Transcript + Migration + Provisional). Once the college finishes
processing, a **pickup receipt** is generated on the student's PU application page;
the student uploads that pickup receipt here with a delivery address. Staff verify it,
collect the certificates from the university, and dispatch them through couriers
(Nepal Can Move, etc.) with tracking shown back to the student.

**Fees:** the catalog shows *our* flat pickup & delivery fee (seeded at Rs. 500,
editable in Django admin), collected as **cash on delivery** by the courier. The PU
fee is paid at services.pu.edu.np and never passes through this site.

Replaces the original NestJS/Prisma API with a single Django project.

## Stack

- Django 6 (session auth, server-rendered templates, Tailwind via CDN)
- PostgreSQL
- Python 3.14

## Workflow / statuses

`Submitted` → `Pickup Receipt Verified` → `Collecting from PU` → `Dispatched` → `Delivered`
(plus `Rejected` for invalid pickup receipts and `Cancelled` by the student).

When staff mark an application **Dispatched** they record the courier
(Nepal Can Move / Fatak / Other) and tracking ID; the cash-on-delivery amount
(the document's service fee) is snapshotted onto the shipment automatically. The
student sees a "Track on Nepal Can Move" link to
[portal.nepalcanmove.com/track](https://portal.nepalcanmove.com/track/) and the COD
amount to pay the courier.

## Bundles (e.g. TMP)

A bundle is just a catalog document whose **includes** field references its component
certificates (admin-created in Django admin → Documents). The seed creates
"TMP Bundle (Transcript + Migration + Provisional)". One bundle application = one PU
application = one pickup receipt; staff see "Bundle includes: …" on the application
detail page.

## Apps

| App | Purpose |
|---|---|
| `pages` | Marketing landing page at `/` |
| `accounts` | Custom user model (email login, roles: Student / Admin / College Staff), register/login/profile |
| `colleges` | College directory |
| `catalog` | Document-type catalog: our service fee, bundles (`includes`), required documents |
| `applications` | Application workflow: pickup-receipt submission, staff pipeline, courier dispatch + COD |

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env   # then edit DB credentials / SECRET_KEY

python manage.py migrate
python manage.py seed   # optional: 3 colleges, 6 documents + TMP bundle (Rs. 500 fee), admin user
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

- `/` — landing page
- `/documents/`, `/documents/<slug>/` — document catalog & detail
- `/colleges/` — college directory
- `/accounts/register|login|logout|profile/`
- `/applications/apply/` — new application (pickup receipt + delivery info)
- `/applications/mine/` — student's applications (with progress timeline)
- `/applications/admin/` — staff dashboard (role: ADMIN / COLLEGE_STAFF)
- `/admin/` — Django admin

## Future work

- Nepal Can Move API integration (auto-create shipment, status sync/webhook) —
  currently manual: staff enter the tracking ID, students deep-link to NCM tracking.
