#!/bin/sh

set -e  # Exit immediately if a command fails

python manage.py migrate --no-input && \
python manage.py collectstatic --no-input && \
exec gunicorn kerocure_backend.kerocure_medical_center.wsgi:application --bind 0.0.0.0:8000
