@echo off
chcp 65001 > nul

cd /d "%~dp0"

echo === [1/3] Проверка и установка зависимостей (PySide6) ===
python -c "import PySide6" 2>nul
if %errorlevel% neq 0 (
    echo PySide6 не найден. Установка...
    pip install PySide6
)

echo === [2/3] Автоматический запуск модульных тестов ===
set PYTHONPATH=src;.
python -m unittest discover -s tests -p "test_*.py"

if %errorlevel% equ 0 (
    echo Тесты пройдены успешно! Запуск эмулятора...
    echo === [3/3] Запуск CMD-UNIXLike-OS Эмулятора ===
    python src/main.py --config config.ini
) else (
    echo Ошибка: Тесты не пройдены. Запуск приложения отменен.
    pause
)