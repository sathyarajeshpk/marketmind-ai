FROM apache/superset:latest

USER root

# Install system deps for postgres driver
RUN apt-get update && apt-get install -y gcc libpq-dev

# Enable pip inside Superset venv
RUN /app/.venv/bin/python -m ensurepip

# Upgrade pip inside venv
RUN /app/.venv/bin/python -m pip install --upgrade pip

# Install psycopg2 inside Superset venv
RUN /app/.venv/bin/python -m pip install psycopg2-binary

COPY superset_config.py /app/superset_config.py
COPY start.sh /app/start.sh

RUN chmod +x /app/start.sh

USER superset

ENV SUPERSET_SECRET_KEY=marketmind-secret-key
ENV SUPERSET_CONFIG_PATH=/app/superset_config.py

ENTRYPOINT ["/app/start.sh"]