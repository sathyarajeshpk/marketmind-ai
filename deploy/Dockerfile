FROM apache/superset:latest

USER root

# Install system dependencies required for psycopg2
RUN apt-get update && apt-get install -y gcc libpq-dev

# Install psycopg2 globally
RUN pip install psycopg2-binary

COPY superset_config.py /app/superset_config.py
COPY start.sh /app/start.sh

RUN chmod +x /app/start.sh

USER superset

ENV SUPERSET_SECRET_KEY=marketmind-secret-key
ENV SUPERSET_CONFIG_PATH=/app/superset_config.py

ENTRYPOINT ["/app/start.sh"]