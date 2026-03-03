FROM apache/superset:latest

USER root
RUN /app/.venv/bin/pip install psycopg2-binary

# Copy custom config
COPY superset_config.py /app/superset_config.py
COPY start.sh /app/start.sh

RUN chmod +x /app/start.sh

USER superset

ENV SUPERSET_SECRET_KEY=marketmind-secret-key
ENV SUPERSET_CONFIG_PATH=/app/superset_config.py

ENTRYPOINT ["/app/start.sh"]