#!/usr/bin/env bash

if [[ "$(docker ps -a | grep app-postgres-1)" ]]; then
  # Get IP of postgres docker container
  postgres_ip=$(
    docker inspect app-postgres-1 \
    | jq -r '.[].NetworkSettings.Networks.app_default.IPAddress'
  )

  if [[ $postgres_ip == null || $postgres_ip == '' ]]; then
    echo 'ERROR: Postgres ip is null'
    exit 1
  fi

  # Replace old database IP
  if sed -i -r 's/DATABASE_HOSTNAME=(\b[0-9]{1,3}\.){3}[0-9]{1,3}\b'/"DATABASE_HOSTNAME=$postgres_ip"/ app/.env; then
    echo "Updated DATABASE_HOSTNAME in app/.env to $postgres_ip"
  fi

  # Start the fastapi backend
  POSTGRES_CONNECTION=app/.env uvicorn app.main:app --reload
else
  echo 'ERROR: Postgres container not running'
fi
