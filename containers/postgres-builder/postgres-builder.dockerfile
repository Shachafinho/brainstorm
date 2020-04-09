FROM postgres
ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD password
ENV POSTGRES_DB brainstorm
COPY resources/init-brainstorm-db.sh /docker-entrypoint-initdb.d/
