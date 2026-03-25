#!/bin/bash
set -e

echo "Waiting for database..."
while ! python -c "
import os, psycopg2
conn = psycopg2.connect(
    dbname=os.environ.get('POSTGRES_DBNAME', 'personal_website'),
    user=os.environ.get('POSTGRES_USER', 'admin_scrape'),
    password=os.environ.get('POSTGRES_PASS', 'my_scraping_test'),
    host=os.environ.get('PG_HOST', 'db'),
    port=os.environ.get('PG_PORT', '5432'),
)
conn.close()
" 2>/dev/null; do
    echo "Database not ready, retrying in 2s..."
    sleep 2
done
echo "Database is ready."

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gunicorn project.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
