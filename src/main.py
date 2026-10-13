import sys
from PySide6.QtWidgets import QApplication

from core.interpreter import CommandInterpreter
from ui.main_window import TerminalWindow


def main():
    """Минимальный прототип эмулятора UNIX (Этап 1)."""
    interpreter = CommandInterpreter()

    app = QApplication(sys.argv)
    window = TerminalWindow(interpreter)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
