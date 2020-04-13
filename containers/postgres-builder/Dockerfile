FROM postgres
ARG RESOURCE_DIR=containers/postgres-builder/resources
ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD password
ENV POSTGRES_DB brainstorm
COPY ${RESOURCE_DIR}/init-brainstorm-db.sh /docker-entrypoint-initdb.d/
