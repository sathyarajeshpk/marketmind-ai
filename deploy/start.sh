#!/bin/bash
set -e

echo "Database URI inside container:"
echo $SQLALCHEMY_DATABASE_URI

echo "Running Superset DB migrations..."
superset db upgrade

echo "Initializing Superset..."
superset init

echo "Starting Gunicorn..."
gunicorn \
  --workers 2 \
  --timeout 120 \
  --bind 0.0.0.0:${PORT:-8088} \
  "superset.app:create_app()"