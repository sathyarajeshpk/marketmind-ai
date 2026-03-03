FROM apache/superset:latest

USER root
RUN pip install psycopg2-binary
USER superset

ENV SUPERSET_SECRET_KEY=marketmind-secret-key
ENV FLASK_ENV=production

CMD gunicorn \
  --workers 2 \
  --timeout 120 \
  --bind 0.0.0.0:${PORT:-8088} \
  "superset.app:create_app()"