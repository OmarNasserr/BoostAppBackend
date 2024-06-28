#!/bin/sh

# Exit on error
set -e

# Collect static files
echo "Collecting static files"
python manage.py collectstatic --noinput

# Make database migrations
echo "Making database migrations"
python manage.py makemigrations

# Apply database migrations
echo "Applying database migrations"
python manage.py migrate

# Start Gunicorn server
echo "Starting Gunicorn"
exec gunicorn BoostApp.wsgi:application --bind 0.0.0.0:$PORT
