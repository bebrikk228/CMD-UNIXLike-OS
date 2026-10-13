import sys
from PySide6.QtWidgets import QApplication

from core.config_manager import ConfigManager
from core.interpreter import CommandInterpreter
from ui.main_window import TerminalWindow


def main():
    """Точка входа эмулятора (Этап 2)."""
    cfg = ConfigManager()
    cfg.initialize()

    interpreter = CommandInterpreter()

    app = QApplication(sys.argv)
    window = TerminalWindow(interpreter)
    window.show()

    window.run_startup_script(cfg)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
