FROM apache/superset:3.0.0

USER root

# Install postgres driver
RUN pip install psycopg2-binary

COPY superset_config.py /app/pythonpath/superset_config.py
COPY start.sh /app/start.sh

RUN chmod +x /app/start.sh

USER superset

ENV SUPERSET_SECRET_KEY=marketmind-secret-key

ENTRYPOINT ["/app/start.sh"]