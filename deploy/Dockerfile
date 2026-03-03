FROM apache/superset:latest

USER root

RUN python -m pip install --upgrade pip
RUN python -m pip install psycopg2-binary

COPY superset_config.py /app/superset_config.py
COPY start.sh /app/start.sh

RUN chmod +x /app/start.sh

USER superset

ENV SUPERSET_SECRET_KEY=marketmind-secret-key
ENV SUPERSET_CONFIG_PATH=/app/superset_config.py

ENTRYPOINT ["/app/start.sh"]