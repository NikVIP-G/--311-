#!/bin/bash

set -e

echo "=== Запуск Personal Finance Manager ==="

# Проверка зависимостей
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен"
    exit 1
fi

if ! command -v xhost &> /dev/null; then
    echo "⚠️  X11 не установлен, GUI может не работать"
fi

# Настройка X11 для Linux/Mac
if [[ "$OSTYPE" == "linux-gnu"* ]] || [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Настройка X11..."
    xhost +local:docker > /dev/null 2>&1 || true

    # Создание xauth файла
    XAUTH=$(mktemp /tmp/.docker.xauth.XXXXXX)
    xauth nlist $DISPLAY | sed -e 's/^..../ffff/' | xauth -f $XAUTH nmerge -
    chmod 644 $XAUTH
    export XAUTHORITY=$XAUTH
fi

# Создание директории для данных
mkdir -p ./data
chmod 777 ./data  # Разрешение на запись для контейнера

echo "Сборка образа..."
docker-compose build

echo "Запуск контейнера..."
docker-compose up -d

echo ""
echo "✅ Приложение запущено!"
echo ""
echo "Для просмотра логов: docker-compose logs -f"
echo "Для остановки: docker-compose down"
echo ""
echo "Данные сохраняются в: ./data"
echo "Через несколько секунд должно появиться окно приложения..."