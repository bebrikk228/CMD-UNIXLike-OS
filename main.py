import sys
from PySide6.QtWidgets import QApplication
from core.config_manager import ConfigManager
from core.interpreter import CommandInterpreter
from core.vfs import VirtualFileSystem
from ui.main_window import TerminalWindow


def main():
    """Точка входа в приложение эмулятора UNIX."""
    cfg = ConfigManager()
    cfg.initialize()

    # Инициализируем VFS и загружаем CSV в память по ТЗ
    vfs = VirtualFileSystem()
    vfs_log = vfs.load_from_csv(cfg.vfs_path)

    interpreter = CommandInterpreter(vfs)

    app = QApplication(sys.argv)
    window = TerminalWindow(interpreter)
    window.show()

    # Отображаем статус ФС в ретро-окне
    window.output_area.append(f"VFS Status: {vfs_log}\n")
    window.run_startup_script(cfg)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
