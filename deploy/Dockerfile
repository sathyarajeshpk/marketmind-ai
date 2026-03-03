FROM apache/superset:latest

USER root
RUN pip install psycopg2-binary

# Copy config + startup script
COPY superset_config.py /app/pythonpath/
COPY start.sh /app/start.sh

RUN chmod +x /app/start.sh

USER superset

ENV SUPERSET_SECRET_KEY=marketmind-secret-key
ENV PYTHONPATH=/app/pythonpath

ENTRYPOINT ["/app/start.sh"]