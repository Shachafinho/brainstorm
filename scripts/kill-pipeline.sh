#!/bin/bash

cd "$(dirname "${BASH_SOURCE[0]}")/.."


declare -a VOLUMES=( \
    "mq-vol" \
    "db-vol" \
)

declare -a CONTAINERS=( \
    "rabbitmq" \
    "postgres" \
    "server" \
    "saver" \
    "parse_user_information" \
    "parse_snapshot" \
    "parse_color_image" \
    "parse_depth_image" \
    "parse_feelings" \
    "parse_pose" \
)

docker stop ${CONTAINERS[@]}
docker rm ${CONTAINERS[@]}

sudo docker network rm my-net
sudo docker volume rm ${VOLUMES[@]}
