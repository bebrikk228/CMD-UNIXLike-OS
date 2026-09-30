import getpass
import os
import socket
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon, QPainter, QPen
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

WIN95_STYLE = """
QWidget#MainContainer {
    background-color: #c0c0c0;
    border-left: 2px solid #fff; border-top: 2px solid #fff;
    border-right: 2px solid #808080; border-bottom: 2px solid #808080;
}
QWidget#TitleBar { background-color: #000080; color: #fff; }
QLabel#TitleText {
    color: #fff; font-weight: bold;
    font-family: "MS Sans Serif", monospace; font-size: 12px;
}
QPushButton#WinBtn {
    background-color: #c0c0c0;
    border-left: 1.5px solid #fff; border-top: 1.5px solid #fff;
    border-right: 1.5px solid #808080; border-bottom: 1.5px solid #808080;
}
QPushButton#WinBtn:pressed {
    border-left: 1.5px solid #808080; border-top: 1.5px solid #808080;
    border-right: 1.5px solid #fff; border-bottom: 1.5px solid #fff;
}
QTextEdit {
    background-color: #000; color: #fff;
    font-family: "Courier New", monospace;
    border-left: 2px solid #808080; border-top: 2px solid #808080;
    border-right: 2px solid #fff; border-bottom: 2px solid #fff;
}
QLineEdit {
    background-color: #fff; color: #000;
    font-family: "Courier New", monospace;
    border-left: 2px solid #808080; border-top: 2px solid #808080;
    border-right: 2px solid #fff; border-bottom: 2px solid #fff;
}
"""


class TerminalWindow(QMainWindow):
    """Графический интерфейс терминала в стиле Windows 95."""

    def __init__(self, interpreter):
        """Инициализация кастомного окна без системных рамок."""
        super().__init__()
        self.interpreter = interpreter

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.resize(650, 420)
        self.setStyleSheet(WIN95_STYLE)

        self.init_ui()

    def init_ui(self):
        """Сборка кастомных виджетов интерфейса."""
        container = QWidget()
        container.setObjectName("MainContainer")
        self.setCentralWidget(container)

        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(4, 4, 4, 4)
        main_layout.setSpacing(4)

        self.create_title_bar(main_layout)
        
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        main_layout.addWidget(self.output_area)

        self.create_input_zone(main_layout)
        self.output_area.append("Microsoft Windows 95\nREPL Прототип готов.\n")

    def create_title_bar(self, layout):
        """Создание ретро-заголовка с кнопками управления."""
        title_bar = QWidget()
        title_bar.setObjectName("TitleBar")
        title_bar.setFixedHeight(22)
        t_layout = QHBoxLayout(title_bar)
        t_layout.setContentsMargins(4, 2, 4, 2)
        t_layout.setSpacing(0)

        username = getpass.getuser()
        hostname = socket.gethostname()
        title_lbl = QLabel(f"  Эмулятор - [{username}@{hostname}]")
        title_lbl.setObjectName("TitleText")
        t_layout.addWidget(title_lbl)

        title_bar.mousePressEvent = self.start_drag
        title_lbl.mousePressEvent = self.start_drag

        self.add_control_buttons(t_layout)
        layout.addWidget(title_bar)

    def add_control_buttons(self, layout):
        """Добавление кнопок с пиксельной геометрической графикой."""
        btn_container = QWidget()
        btn_layout = QHBoxLayout(btn_container)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setSpacing(2)

        icon_min = self.draw_icon("min")
        icon_max = self.draw_icon("max")
        icon_close = self.draw_icon("close")

        btn_layout.addWidget(self.make_btn(icon_min, self.showMinimized))
        btn_layout.addWidget(self.make_btn(icon_max, self.toggle_maximize))
        btn_layout.addWidget(self.make_btn(icon_close, self.close))

        layout.addWidget(btn_container, alignment=Qt.AlignmentFlag.AlignRight)

    def make_btn(self, icon: QIcon, slot) -> QPushButton:
        """Фабрика для создания аккуратных ретро-кнопок."""
        btn = QPushButton()
        btn.setObjectName("WinBtn")
        btn.setFixedSize(16, 14)
        btn.setIcon(icon)
        btn.setIconSize(QSize(16, 14))
        btn.clicked.connect(slot)
        return btn

    def draw_icon(self, mode: str) -> QIcon:
        """Отрисовка пиксельных иконок элементов управления."""
        from PySide6.QtGui import QPixmap
        pixmap = QPixmap(16, 14)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        pen = QPen(Qt.GlobalColor.black, 1, Qt.PenStyle.SolidLine)
        painter.setPen(pen)

        if mode == "min":
            painter.drawLine(3, 10, 8, 10)
        elif mode == "max":
            painter.drawRect(3, 3, 9, 7)
            painter.drawLine(3, 4, 12, 4)
        elif mode == "close":
            painter.drawLine(4, 3, 10, 9)
            painter.drawLine(5, 3, 11, 9)
            painter.drawLine(4, 9, 10, 3)
            painter.drawLine(5, 9, 11, 3)

        painter.end()
        return QIcon(pixmap)

    def create_input_zone(self, layout):
        """Создание интуитивной зоны ввода с кнопкой Выполнить."""
        input_layout = QHBoxLayout()
        input_layout.setSpacing(4)

        self.input_field = QLineEdit()
        self.input_field.returnPressed.connect(self.handle_input)
        input_layout.addWidget(self.input_field)

        run_btn = QPushButton("Выполнить")
        run_btn.setObjectName("WinBtn")
        run_btn.setFixedSize(90, 22)
        run_btn.clicked.connect(self.handle_input)
        input_layout.addWidget(run_btn)

        layout.addLayout(input_layout)

    def run_startup_script(self, config_manager):
        """Запуск стартового скрипта с имитацией диалога."""
        self.output_area.append(config_manager.get_debug_info())
        script_path = config_manager.script_path
        
        if not script_path:
            return
        if not os.path.exists(script_path):
            self.output_area.append(f"Script Error: '{script_path}' missing.\n")
            return

        self.output_area.append(f"--- Running script: {script_path} ---")
        with open(script_path, "r", encoding="utf-8") as f:
            for line in f:
                raw_line = line.strip()
                if not raw_line or raw_line.startswith("#"):
                    continue
                
                self.output_area.append(f"$ {raw_line}")
                response, should_exit = self.interpreter.execute(raw_line)
                
                if response:
                    self.output_area.append(response)
                if should_exit:
                    self.close()
                    return
        self.output_area.append("--- Script execution finished ---\n")

    def toggle_maximize(self):
        """Переключение между полноэкранным и оконным режимом."""
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def start_drag(self, event):
        """Запуск системного перемещения окна (Wayland/Windows)."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.windowHandle().startSystemMove()
            event.accept()

    def handle_input(self):
        """Обработка ручного ввода команды пользователя."""
        text = self.input_field.text()
        if not text:
            return

        self.output_area.append(f"$ {text}")
        response, should_exit = self.interpreter.execute(text)

        if response:
            self.output_area.append(response)

        self.input_field.clear()
        if should_exit:
            self.close()
