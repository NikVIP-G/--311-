#!/bin/bash
# stop.sh

CONTAINER_NAME="personal-finance"

echo "Остановка контейнера $CONTAINER_NAME..."
docker stop $CONTAINER_NAME 2>/dev/null && echo "✅ Контейнер остановлен" || echo "Контейнер не найден"

echo "Удаление контейнера..."
docker rm $CONTAINER_NAME 2>/dev/null && echo "✅ Контейнер удален" || echo "Контейнер не найден"