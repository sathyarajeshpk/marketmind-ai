FROM apache/superset:latest

USER root

RUN pip install psycopg2-binary

USER superset

ENV SUPERSET_SECRET_KEY=marketmind-secret-key

CMD superset db upgrade && \
    superset fab create-admin \
    --username admin \
    --firstname Admin \
    --lastname User \
    --email admin@marketmind.ai \
    --password admin123 && \
    superset init && \
    superset run -h 0.0.0.0 -p 8088