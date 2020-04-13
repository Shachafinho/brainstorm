#!/bin/bash

set -e
cd "$(dirname "${BASH_SOURCE[0]}")/.."


NETWORK_NAME="my-net"

MQ_VOLUME_NAME="mq-vol"
MQ_VOLUME_TARGET="/workspace/mq_data"
DB_VOLUME_NAME="db-vol"

MQ_NAME="rabbitmq"
MQ_PORT=5672
MQ_URL="rabbitmq://$MQ_NAME:$MQ_PORT/"
DB_NAME="postgres"
DB_PORT=5432
DB_URL="postgresql://$DB_NAME:$DB_PORT/"
SERVER_PORT=8000

declare -a PARSERS=( \
    "user_information" \
    "snapshot" \
    "color_image" \
    "depth_image" \
    "feelings" \
    "pose" \
)


function build_container {
    container_name=$1
    (export DOCKER_BUILDKIT=1; docker build . \
        -t $container_name \
        -f containers/$container_name/Dockerfile)
}

function container_running {
    container_name=$1
    container_id="$(docker container ls | grep $container_name | awk '{ print $1 }')"
    [ -n "$container_id" ]
    is_running=$?
    return $is_running
}

build_container "postgres-builder"
build_container "brainstorm-builder"


docker volume create $MQ_VOLUME_NAME
docker volume create $DB_VOLUME_NAME
docker network create $NETWORK_NAME

WAITING_REQUIRED=false
if ! container_running $MQ_NAME; then
    echo "Running docker container: $MQ_NAME"
    docker run -d -p $MQ_PORT:$MQ_PORT --name $MQ_NAME --network $NETWORK_NAME rabbitmq
    WAITING_REQUIRED=true
fi
if ! container_running $DB_NAME; then
    echo "Running docker container: $DB_NAME"
    docker run -d -p $DB_PORT:$DB_PORT \
        --name $DB_NAME \
        --network $NETWORK_NAME \
        --mount source=$DB_VOLUME_NAME,target=/var/lib/postgresql/data \
        postgres-builder
    WAITING_REQUIRED=true
fi
if [ "$WAITING_REQUIRED" = true ]; then
    echo "Waiting for containers to setup..."
    sleep 10
fi

if ! container_running server; then
    echo "Running docker container: server"
    docker run -d -t -p $SERVER_PORT:$SERVER_PORT \
        --name server \
        --network $NETWORK_NAME \
        --mount source=$MQ_VOLUME_NAME,target=$MQ_VOLUME_TARGET \
        brainstorm-builder \
        python -m brainstorm.server run-server "$MQ_URL" --host "0.0.0.0"
fi
if ! container_running saver; then
    echo "Running docker container: saver"
    docker run -d -t \
        --name saver \
        --network $NETWORK_NAME \
        --mount source=$MQ_VOLUME_NAME,target=$MQ_VOLUME_TARGET \
        --mount source=$DB_VOLUME_NAME,target=/workspace/db_data \
        brainstorm-builder \
        python -m brainstorm.saver run-saver "$DB_URL" "$MQ_URL"
fi
for parser_name in ${PARSERS[@]}; do
    PARSER_CONTAINER="parse_$parser_name"
    if ! container_running $PARSER_CONTAINER; then
        echo "Running docker container: $PARSER_CONTAINER"
        docker run -d -t \
            --name $PARSER_CONTAINER \
            --network $NETWORK_NAME \
            --mount source=$MQ_VOLUME_NAME,target=$MQ_VOLUME_TARGET \
            brainstorm-builder \
            python -m brainstorm.parsers run-parser "$parser_name" "$MQ_URL"
    fi
done
