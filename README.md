# Personal Website — Ahmad Zaenun Faiz

A Django-based personal portfolio website showcasing projects, work experience, certifications, skills, and a contact form.

## Architecture

```
website/
├── project/              # Django project — settings + app code
│   ├── settings.py       # All config — reads from env vars directly
│   ├── urls.py
│   ├── wsgi.py
│   ├── geoip/            # GeoLite2 .mmdb databases (for activity logging)
│   └── home/             # Home app — models, views, signals, admin, forms
│       ├── models.py
│       ├── views.py
│       ├── signals.py
│       ├── admin.py
│       ├── forms.py
│       ├── urls.py
│       ├── apps.py
│       └── migrations/
├── templates/            # All templates (base, home partials, auth, error pages)
├── static/               # CSS, JS, images, fonts
├── media/                # User-uploaded files (portfolio images, certificates)
├── Dockerfile
├── docker-compose.yml
├── docker-entrypoint.sh
└── requirements.txt
```

## Features

- **Portfolio** — project showcase with framework tags
- **Experience** — work history timeline
- **Certificates** — certification cards with links
- **Skills** — skill grid with icons
- **Contact Form** — with Google ReCAPTCHA and email notification via SMTP
- **Activity Logging** — tracks login/logout events with device/browser/GeoIP info
- **Admin Interface** — customized Django admin with filters and array field support

## Tech Stack

- **Backend:** Django 5.2, Gunicorn
- **Database:** PostgreSQL 16
- **Frontend:** Bootstrap 5, Crispy Forms
- **Containerization:** Docker, Docker Compose

## Getting Started

### Prerequisites

- Docker and Docker Compose

### Setup

1. Clone the repository:
   ```bash
   git clone <repo-url> && cd website
   ```

2. Create a `.env` file (or edit the existing one):
   ```env
   # PostgreSQL
   PG_HOST=db
   PG_PORT=5432
   POSTGRES_USER=faiz_admin
   POSTGRES_PASS=<your-password>
   POSTGRES_DBNAME=faiz_website

   # Django
   SECRET_KEY=<your-secret-key>
   DEBUG=true
   ALLOWED_HOSTS=localhost|127.0.0.1

   # Email SMTP
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=true
   EMAIL_HOST_USER=<your-email>
   EMAIL_HOST_PASSWORD=<your-app-password>

   # Google ReCAPTCHA
   RECAPTCHA_PUBLIC_KEY=<your-public-key>
   RECAPTCHA_PRIVATE_KEY=<your-private-key>
   ```

3. (Optional) Place GeoIP databases in `project/geoip/`:
   - `GeoLite2-ASN.mmdb`
   - `GeoLite2-City.mmdb`

   These are needed for activity logging on login events. Download from [MaxMind](https://dev.maxmind.com/geoip/geolite2-free-geolocation-data).

4. Build and run:
   ```bash
   docker compose up --build
   ```

5. Create a superuser:
   ```bash
   docker compose exec web python manage.py createsuperuser
   ```

6. Open the site at `http://localhost:8000` and admin at `http://localhost:8000/admin/`.

### Local Development (without Docker)

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Requires a local PostgreSQL instance. Configure connection via environment variables.

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `SECRET_KEY` | Django secret key | `change-me-in-production` |
| `DEBUG` | Debug mode | `true` |
| `ALLOWED_HOSTS` | Allowed hosts (`\|` separated) | `localhost` |
| `CSRF_TRUSTED_ORIGINS` | CSRF trusted origins (`\|` separated) | — |
| `PG_HOST` | Database host | `127.0.0.1` |
| `PG_PORT` | Database port | `5432` |
| `POSTGRES_USER` | Database user | `faiz_admin` |
| `POSTGRES_PASS` | Database password | — |
| `POSTGRES_DBNAME` | Database name | `personal_website` |
| `EMAIL_HOST_USER` | SMTP sender email | — |
| `EMAIL_HOST_PASSWORD` | SMTP app password | — |
| `RECAPTCHA_PUBLIC_KEY` | ReCAPTCHA site key | — |
| `RECAPTCHA_PRIVATE_KEY` | ReCAPTCHA secret key | — |
