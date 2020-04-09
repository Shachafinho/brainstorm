#!/bin/bash

set -e
cd "$(dirname "${BASH_SOURCE[0]}")/.."


sudo docker stop rabbitmq postgres
sudo docker rm rabbitmq postgres
