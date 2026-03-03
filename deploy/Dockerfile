FROM apache/superset:latest

USER root
RUN pip install psycopg2-binary
USER superset

ENV SUPERSET_SECRET_KEY=marketmind-secret-key
ENV FLASK_ENV=production

CMD /bin/bash -c "
superset db upgrade &&
superset fab create-admin \
    --username admin \
    --firstname Admin \
    --lastname User \
    --email admin@marketmind.ai \
    --password admin123 || true &&
superset init &&
gunicorn \
  --workers 2 \
  --timeout 120 \
  --bind 0.0.0.0:${PORT:-8088} \
  'superset.app:create_app()'
"