import sys
from PySide6.QtWidgets import QApplication
from core.config_manager import ConfigManager
from core.interpreter import CommandInterpreter
from ui.main_window import TerminalWindow


def main():
    """Точка входа в приложение эмулятора."""
    # 1. Считываем конфигурацию и приоритеты по ТЗ
    cfg = ConfigManager()
    cfg.initialize()

    app = QApplication(sys.argv)

    interpreter = CommandInterpreter()
    window = TerminalWindow(interpreter)
    window.show()

    # 2. Передаем управление скрипту после отрисовки окна
    window.run_startup_script(cfg)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
