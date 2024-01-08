#!/bin/bash

echo "start docker container"
docker compose up -d &
sleep 5
wait
echo "start web app"
cd frontend/app && npm start &
wait
exit $?
