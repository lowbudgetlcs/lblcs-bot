#!/bin/bash

docker compose down && \
docker build -t lblcs/discord-bot . && \
docker compose up
