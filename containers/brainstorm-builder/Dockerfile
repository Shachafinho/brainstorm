FROM python:3
ARG RESOURCE_DIR=.
WORKDIR /workspace
COPY ${RESOURCE_DIR}/requirements.txt .
RUN pip install -r requirements.txt
COPY ${RESOURCE_DIR}/brainstorm brainstorm
