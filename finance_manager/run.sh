#!/bin/bash
# run.sh

set -e

# Имя образа и контейнера
IMAGE_NAME="finance-app"
CONTAINER_NAME="personal-finance"

echo "=== Запуск Personal Finance Manager ==="

# Останавливаем и удаляем старый контейнер
docker stop $CONTAINER_NAME 2>/dev/null || true
docker rm $CONTAINER_NAME 2>/dev/null || true

# Собираем образ
echo "Сборка Docker образа..."
docker build -t $IMAGE_NAME .

# Создаем директорию для данных
mkdir -p ./data

# Определяем параметры запуска в зависимости от ОС
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Linux detected"
    # Настраиваем X11
    xhost +local:docker 2>/dev/null
    xhost +local:root 2>/dev/null

    X11_OPTS="-v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY --network host"

elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "macOS detected"
    # Для Mac с Docker Desktop
    X11_OPTS="-e DISPLAY=host.docker.internal:0"

elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo "Windows detected"
    # Для Windows с WSL2
    export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0
    X11_OPTS="-e DISPLAY=$DISPLAY"
else
    echo "Unknown OS, running in headless mode"
    X11_OPTS=""
fi

# Запускаем контейнер
echo "Запуск контейнера..."
docker run -d \
  --name $CONTAINER_NAME \
  -v $(pwd)/data:/root/.personal_finance_manager \
  $X11_OPTS \
  $IMAGE_NAME

echo ""
echo "✅ Контейнер запущен: $CONTAINER_NAME"
echo ""
echo "Команды для управления:"
echo "  docker logs -f $CONTAINER_NAME    # Просмотр логов"
echo "  docker exec -it $CONTAINER_NAME bash  # Вход в контейнер"
echo "  docker stop $CONTAINER_NAME       # Остановка"
echo ""
echo "Приложение должно запуститься через несколько секунд..."