@echo off
chcp 65001 > nul
echo === [1/3] Проверка и установка зависимостей (PySide6) ===
python -c "import PySide6" 2>nul
if %errorlevel% neq 0 (
    echo PySide6 не найден. Установка...
    pip install PySide6
)

echo === [2/3] Автоматический запуск модульных тестов ===
python -m unittest discover tests

if %errorlevel% equ 0 (
    echo Тесты пройдены успешно! Запуск эмулятора...
    echo === [3/3] Запуск CMD-UNIXLike-OS Эмулятора ===
    python main.py --config config.ini
) else (
    echo Ошибка: Тесты не пройдены. Запуск приложения отменен.
    pause
)
