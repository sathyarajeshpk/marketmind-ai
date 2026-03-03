FROM apache/superset:3.1.0

USER root

# Install postgres driver
RUN pip install psycopg2-binary

USER superset

ENV SUPERSET_SECRET_KEY=marketmind_secret_key

EXPOSE 8088

CMD superset db upgrade && \
    superset init && \
    superset run -h 0.0.0.0 -p 8088