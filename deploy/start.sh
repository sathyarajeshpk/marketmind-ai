#!/bin/bash
set -e

echo "Running Superset DB migrations..."
superset db upgrade

echo "Initializing Superset..."
superset init

echo "Starting Gunicorn..."

exec gunicorn \
  --workers 1 \
  --threads 2 \
  --worker-class gthread \
  --timeout 120 \
  --bind 0.0.0.0:$PORT \
  "superset.app:create_app()"