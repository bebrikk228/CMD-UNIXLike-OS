import argparse
import configparser
import os


class ConfigManager:
    """Менеджер для обработки аргументов командной строки и INI конфига."""

    def __init__(self):
        """Инициализация пустых путей."""
        self.vfs_path = ""
        self.script_path = ""

    def parse_args(self) -> argparse.Namespace:
        """Парсинг аргументов командной строки."""
        parser = argparse.ArgumentParser(description="Unix Emulator Config")
        parser.add_argument("--vfs", type=str, default="", help="VFS path")
        parser.add_argument("--script", type=str, default="", help="Script")
        parser.add_argument("--config", type=str, default="", help="INI config")
        return parser.parse_args()

    def load_ini(self, ini_path: str):
        """Загрузка настроек из INI файла с проверкой существования."""
        if not ini_path or not os.path.exists(ini_path):
            return

        config = configparser.ConfigParser()
        config.read(ini_path)

        if "Setting" in config:
            sec = config["Setting"]
            # По ТЗ: значения из файла имеют приоритет
            self.vfs_path = sec.get("vfs_path", self.vfs_path)
            self.script_path = sec.get("script_path", self.script_path)

    def initialize(self):
        """Сборка параметров согласно логике приоритетов ТЗ."""
        args = self.parse_args()

        # Сначала берем базовые аргументы из командной строки
        self.vfs_path = args.vfs
        self.script_path = args.script

        # Если передан конфиг-файл, он перепишет аргументы строки
        if args.config:
            self.load_ini(args.config)

    def get_debug_info(self) -> str:
        """Формирование строки отладочного вывода всех параметров."""
        info = (
            f"--- DEBUG CONFIG INFO ---\n"
            f"VFS Location: {self.vfs_path or 'Not specified'}\n"
            f"Start Script: {self.script_path or 'Not specified'}\n"
            f"-------------------------\n"
        )
        return info
