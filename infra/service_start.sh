#!/bin/bash

echo "Building docker images"
docker compose --profile server build -q

echo "Starting services"
docker compose --profile server up -d --quiet-pull
