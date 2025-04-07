#!/bin/sh

echo "Wait for Database..."

while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  sleep 1
done

echo "Database is ready! Migrate..."
python manage.py migrate

echo "Run server..."
python manage.py runserver 0.0.0.0:8000
