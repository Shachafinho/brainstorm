#!/bin/bash

set -e
cd "$(dirname "${BASH_SOURCE[0]}")/.."


function build_container {
    container_name=$1
    pushd containers/$container_name/
    docker build . \
        -t $container_name \
        -f $container_name.dockerfile
    popd
}

function container_running {
    container_name=$1
    container_id="$(docker container ls | grep $container_name | awk '{ print $1 }')"
    [ ! -z "$container_id" ]
    return $?
}

build_container "postgres-builder"


container_running rabbitmq || docker run -d -p 5672:5672 --name rabbitmq rabbitmq
# docker run -d -p 5432:5432 --name postgres \
#     -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=password -e POSTGRES_DB=brainstorm \
#     postgres
container_running postgres || docker run -d -p 5432:5432 --name postgres postgres-builder
