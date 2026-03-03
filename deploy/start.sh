#!/bin/bash
set -e

echo "Creating Admin User..."

superset fab create-admin \
    --username admin \
    --firstname Admin \
    --lastname User \
    --email admin@marketmind.ai \
    --password admin123

echo "Starting Gunicorn..."

exec gunicorn \
  --workers 1 \
  --threads 2 \
  --worker-class gthread \
  --timeout 120 \
  --bind 0.0.0.0:$PORT \
  "superset.app:create_app()"