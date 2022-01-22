#!/usr/bin/env bash

# Get IP of postgres docker container
postgres_ip=$(
  docker inspect fastapitest-postgres-1 \
  | jq -r '.[].NetworkSettings.Networks.fastapitest_default.IPAddress'
)

# Replace old database IP
if sed -i -r 's/DATABASE_HOSTNAME=(\b[0-9]{1,3}\.){3}[0-9]{1,3}\b'/"DATABASE_HOSTNAME=$postgres_ip"/ app/.env; then
  echo "Updated DATABASE_HOSTNAME in app/.env to $postgres_ip"
fi

# Start the fastapi backend
POSTGRES_CONNECTION=app/.env uvicorn app.main:app --reload
