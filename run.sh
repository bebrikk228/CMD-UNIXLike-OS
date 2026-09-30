#!/bin/bash

echo "=== [1/3] Проверка и установка зависимостей (PySide6) ==="
# Устанавливаем PySide6 пользователя, если его нет
python3 -c "import PySide6" 2>/dev/null || pip install --user PySide6

echo "=== [2/3] Автоматический запуск модульных тестов ==="
python3 -m unittest discover tests

if [ $? -eq 0 ]; then
    echo "Тесты пройдены успешно! Запуск эмулятора..."
    echo "=== [3/3] Запуск CMD-UNIXLike-OS Эмулятора ==="
    # Запускаем приложение со ссылкой на INI конфиг
    python3 main.py --config config.ini
else
    echo "Ошибка: Тесты не пройдены. Запуск приложения отменен."
    exit 1
fi
