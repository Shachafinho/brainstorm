#!/bin/bash

set -e
cd "$(dirname "${BASH_SOURCE[0]}")/.."


NETWORK_NAME="my-net"

MQ_VOLUME_NAME="mq-vol"
MQ_VOLUME_TARGET="/workspace/mq_data"
DB_VOLUME_NAME="db-vol"
DB_VOLUME_TARGET="/workspace/db_data"

MQ_NAME="rabbitmq"
MQ_PORT=5672
MQ_URL="rabbitmq://$MQ_NAME:$MQ_PORT/"
DB_NAME="postgres"
DB_PORT=5432
DB_URL="postgresql://$DB_NAME:$DB_PORT/"
SERVER_PORT=8000
API_SERVER_PORT=5000

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

function is_up {
    component=$1
    component_name=$2
    [ -n "$(docker $component ls -f name=\^$component_name\$ | tail -n +2)" ]
}

build_container "postgres-builder"
build_container "brainstorm-builder"


echo "Setting up volumes"
if ! is_up volume $MQ_VOLUME_NAME; then
    docker volume create $MQ_VOLUME_NAME
fi
if ! is_up volume $DB_VOLUME_NAME; then
    docker volume create $DB_VOLUME_NAME
fi

echo "Setting up networks"
if ! is_up network $NETWORK_NAME; then
    docker network create $NETWORK_NAME
fi

echo "Setting up containers"
WAITING_REQUIRED=false
if ! is_up container $MQ_NAME; then
    echo "Running docker container: $MQ_NAME"
    docker run -d -p $MQ_PORT:$MQ_PORT --name $MQ_NAME --network $NETWORK_NAME rabbitmq
    WAITING_REQUIRED=true
fi
if ! is_up container $DB_NAME; then
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

if ! is_up container api_server; then
    echo "Running docker container: api_server"
    docker run -d -t -p $API_SERVER_PORT:$API_SERVER_PORT \
        --name api_server \
        --network $NETWORK_NAME \
        --mount source=$DB_VOLUME_NAME,target=$DB_VOLUME_TARGET \
        brainstorm-builder \
        python -m brainstorm.api run-server --host "0.0.0.0" --database "$DB_URL"
fi
if ! is_up container saver; then
    echo "Running docker container: saver"
    docker run -d -t \
        --name saver \
        --network $NETWORK_NAME \
        --mount source=$MQ_VOLUME_NAME,target=$MQ_VOLUME_TARGET \
        --mount source=$DB_VOLUME_NAME,target=$DB_VOLUME_TARGET \
        brainstorm-builder \
        python -m brainstorm.saver run-saver "$DB_URL" "$MQ_URL"
fi
for parser_name in ${PARSERS[@]}; do
    PARSER_CONTAINER="parse_$parser_name"
    if ! is_up container $PARSER_CONTAINER; then
        echo "Running docker container: $PARSER_CONTAINER"
        docker run -d -t \
            --name $PARSER_CONTAINER \
            --network $NETWORK_NAME \
            --mount source=$MQ_VOLUME_NAME,target=$MQ_VOLUME_TARGET \
            brainstorm-builder \
            python -m brainstorm.parsers run-parser "$parser_name" "$MQ_URL"
    fi
done
if ! is_up container server; then
    echo "Running docker container: server"
    docker run -d -t -p $SERVER_PORT:$SERVER_PORT \
        --name server \
        --network $NETWORK_NAME \
        --mount source=$MQ_VOLUME_NAME,target=$MQ_VOLUME_TARGET \
        brainstorm-builder \
        python -m brainstorm.server run-server --host "0.0.0.0" "$MQ_URL"
fi
