#!/bin/bash

cd "$(dirname "${BASH_SOURCE[0]}")/.."


declare -a VOLUMES=( \
    "mq-vol" \
    "db-vol" \
)

declare -a CONTAINERS=( \
    "rabbitmq" \
    "postgres" \
    "api_server" \
    "saver" \
    "parse_user_information" \
    "parse_snapshot" \
    "parse_color_image" \
    "parse_depth_image" \
    "parse_feelings" \
    "parse_pose" \
    "server" \
)

docker stop ${CONTAINERS[@]}
docker rm ${CONTAINERS[@]}

# Uncomment the following lines to remove the networks and volumes as well
# sudo docker network rm my-net
# CAUTION: Removing the volumes means deleting EVERYTHING from the DB.
# sudo docker volume rm ${VOLUMES[@]}
