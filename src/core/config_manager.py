import argparse
import configparser
import os


class ConfigManager:
    """Менеджер для обработки аргументов командной строки и INI конфига."""

    def __init__(self):
        """Инициализация путей конфигурации."""
        self.vfs_path = ""
        self.script_path = ""

    def parse_args(self) -> argparse.Namespace:
        """Парсинг аргументов командной строки."""
        parser = argparse.ArgumentParser(description="Unix Emulator Config")
        parser.add_argument("--vfs", type=str, default="", help="VFS path")
        parser.add_argument("--script", type=str, default="", help="Script")
        parser.add_argument("--config", type=str, default="", help="INI config")
        return parser.parse_args()

    def load_ini(self, ini_path: str) -> bool:
        """Загрузка настроек из INI файла с проверкой существования."""
        if not ini_path:
            return True
        if not os.path.exists(ini_path):
            print(f"Config Error: Конфигурационный файл '{ini_path}' не найден.")
            return False

        try:
            config = configparser.ConfigParser()
            config.read(ini_path, encoding="utf-8")

            if "Setting" in config:
                sec = config["Setting"]
                self.vfs_path = sec.get("vfs_path", self.vfs_path)
                self.script_path = sec.get("script_path", self.script_path)
            return True
        except Exception as e:
            print(f"Config Error: Ошибка чтения INI файла ({e}).")
            return False

    def initialize(self):
        """Сборка параметров согласно логике приоритетов ТЗ."""
        args = self.parse_args()

        self.vfs_path = args.vfs
        self.script_path = args.script

        if args.config:
            self.load_ini(args.config)

    def get_debug_info(self) -> str:
        """Формирование строки отладочного вывода параметров."""
        return (
            "--- DEBUG CONFIG INFO ---\n"
            f"VFS Location: {self.vfs_path or 'Not specified'}\n"
            f"Start Script: {self.script_path or 'Not specified'}\n"
            "-------------------------\n"
        )
