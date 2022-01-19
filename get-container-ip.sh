#!/usr/bin/env bash
container="$1"

if [[ -z "$container" ]]; then
  echo 'Please provide the container ID as the first argument'
  exit 1
fi

docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' "$container"