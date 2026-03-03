#!/bin/bash

echo "Database URI inside container:"
echo $SQLALCHEMY_DATABASE_URI

echo "Running Superset DB migrations..."
superset db upgrade

echo "Initializing Superset..."
superset init

echo "Starting Superset..."

gunicorn \
  --workers 1 \
  --threads 2 \
  --timeout 120 \
  --bind 0.0.0.0:$PORT \
  "superset.app:create_app()"