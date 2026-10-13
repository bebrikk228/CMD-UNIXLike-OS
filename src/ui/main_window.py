import getpass
import os
import socket

from PySide6.QtCore import QPoint, QSize, Qt
from PySide6.QtGui import QBrush, QIcon, QPainter, QPen, QPixmap
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class Win95ScrollHandle(QPushButton):
    """Кастомный ползунок с поддержкой плавного перетаскивания мышкой."""

    def __init__(self, parent_window: QMainWindow, slider_zone: QWidget):
        super().__init__()
        self.win = parent_window
        self.zone = slider_zone
        self.setObjectName("ScrollHandle")
        self.setFixedWidth(16)
        self.drag_start_y = 0
        self.margin_start_y = 0

    def mousePressEvent(self, event):
        """Фиксация точки нажатия мыши."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start_y = event.globalPosition().y()
            self.margin_start_y = self.zone.layout().contentsMargins().top()
            event.accept()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """Расчет математической пропорции прокрутки при перетаскивании."""
        if event.buttons() & Qt.MouseButton.LeftButton:
            delta_y = event.globalPosition().y() - self.drag_start_y
            new_margin = max(0, self.margin_start_y + int(delta_y))

            available_space = self.zone.height() - self.height()
            if available_space > 0:
                new_margin = min(new_margin, available_space)
                ratio = new_margin / available_space
                src_sb = self.win.output_area.verticalScrollBar()
                val_range = src_sb.maximum() - src_sb.minimum()
                src_sb.setValue(int(src_sb.minimum() + ratio * val_range))
            event.accept()
        super().mouseMoveEvent(event)


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

/* ЕДИНЫЙ СТАНДАРТ РЕТРО-КНОПОК (Окно, Скроллбар, Стрелочка) */
QPushButton#WinBtn, QPushButton#ScrollHandle, QPushButton#RunBtn {
    background-color: #c0c0c0; color: #000000 !important; font-weight: bold;
    font-family: "MS Sans Serif", monospace; font-size: 11px;
    border-left: 1.5px solid #fff; border-top: 1.5px solid #fff;
    border-right: 1.5px solid #808080; border-bottom: 1.5px solid #808080;
}
QPushButton#WinBtn:pressed, QPushButton#ScrollHandle:pressed, QPushButton#RunBtn:pressed {
    border-left: 1.5px solid #808080; border-top: 1.5px solid #808080;
    border-right: 1.5px solid #fff; border-bottom: 1.5px solid #fff;
}

/* Текстовые поля и инпуты (Единый вдавленный 3D рельеф) */
QTextEdit, QLineEdit, QLabel#PromptLabel {
    border-left: 2px solid #808080; border-top: 2px solid #808080;
    border-right: 2px solid #fff; border-bottom: 2px solid #fff;
}
QTextEdit { background-color: #000; color: #fff; font-family: "Courier New", monospace; }
QLineEdit { background-color: #fff; color: #000; font-family: "Courier New", monospace; }
QLabel#PromptLabel {
    color: #000000; font-family: "Courier New", monospace; font-weight: bold;
    font-size: 12px; padding-left: 4px; padding-right: 4px; background-color: #c0c0c0;
}

/* Трек бесшовно прилегает к QTextEdit без внутренних щелей */
QWidget#ScrollTrack {
    background-color: #dfdfdf;
    border-top: 2px solid #808080;
    border-bottom: 2px solid #fff;
    border-right: 2px solid #fff;
    border-left: none;
}
"""


class TerminalWindow(QMainWindow):
    """Графический интерфейс терминала в стиле Windows 95."""

    def __init__(self, interpreter):
        super().__init__()
        self.interpreter = interpreter
        self.username = getpass.getuser()
        self.hostname = socket.gethostname()
        self._icon_cache = {}

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.resize(650, 450)
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

        center_layout = QHBoxLayout()
        center_layout.setSpacing(0)

        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        self.output_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        center_layout.addWidget(self.output_area)

        self.create_custom_win95_scrollbar(center_layout)
        main_layout.addLayout(center_layout)

        self.create_two_level_input_zone(main_layout)
        self.output_area.append("Microsoft Windows 95\nSystem Ready.\n")
        self.update_prompt_label()

    def create_custom_win95_scrollbar(self, layout: QHBoxLayout):
        """Создание ретро-скроллбара с поддержкой удержания кнопок."""
        self.track = QWidget()
        self.track.setObjectName("ScrollTrack")
        self.track.setFixedWidth(18)

        track_layout = QVBoxLayout(self.track)
        track_layout.setContentsMargins(0, 0, 0, 0)
        track_layout.setSpacing(0)

        def setup_scroll_button(btn: QPushButton):
            btn.setObjectName("WinBtn")
            btn.setFixedSize(16, 16)
            btn.setIconSize(QSize(16, 16))
            btn.setAutoRepeat(True)
            btn.setAutoRepeatDelay(300)
            btn.setAutoRepeatInterval(40)

        btn_up = QPushButton()
        setup_scroll_button(btn_up)
        btn_up.setIcon(self.draw_icon("arrow_up"))
        track_layout.addWidget(
            btn_up,
            alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter,
        )

        self.slider_zone = QWidget()
        self.slider_zone.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        self.slider_layout = QVBoxLayout(self.slider_zone)
        self.slider_layout.setContentsMargins(0, 0, 0, 0)
        self.slider_layout.setSpacing(0)

        self.handle = Win95ScrollHandle(self, self.slider_zone)
        self.slider_layout.addWidget(
            self.handle,
            alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter,
        )

        track_layout.addWidget(self.slider_zone)

        btn_down = QPushButton()
        setup_scroll_button(btn_down)
        btn_down.setIcon(self.draw_icon("arrow_down"))
        track_layout.addWidget(
            btn_down,
            alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter,
        )

        src_sb = self.output_area.verticalScrollBar()
        src_sb.rangeChanged.connect(self._sync_scrollbar_geometry)
        src_sb.valueChanged.connect(self._sync_scrollbar_position)

        btn_up.clicked.connect(lambda: src_sb.setValue(src_sb.value() - 15))
        btn_down.clicked.connect(lambda: src_sb.setValue(src_sb.value() + 15))

        self.track.setVisible(False)
        layout.addWidget(self.track)

    def _sync_scrollbar_geometry(self, min_val: int, max_val: int):
        """Динамический расчет высоты ползунка."""
        src_sb = self.output_area.verticalScrollBar()
        self.track.setVisible(max_val > min_val)

        total_range = max_val - min_val + src_sb.pageStep()
        if total_range > 0:
            ratio = src_sb.pageStep() / total_range
            available_h = max(100, self.slider_zone.height())
            new_h = max(20, int(available_h * ratio))
            self.handle.setFixedHeight(new_h)

    def _sync_scrollbar_position(self, value: int):
        """Синхронизация положения ползунка."""
        src_sb = self.output_area.verticalScrollBar()
        min_v = src_sb.minimum()
        max_v = src_sb.maximum()

        if max_v > min_v:
            ratio = (value - min_v) / (max_v - min_v)
            available_space = self.slider_zone.height() - self.handle.height()
            top_margin = int(available_space * ratio)
            self.slider_layout.setContentsMargins(0, top_margin, 0, 0)

    def create_title_bar(self, layout: QVBoxLayout):
        """Создание ретро-заголовка с названиями по ТЗ Варианта 28."""
        title_bar = QWidget()
        title_bar.setObjectName("TitleBar")
        title_bar.setFixedHeight(22)
        t_layout = QHBoxLayout(title_bar)
        t_layout.setContentsMargins(4, 2, 4, 2)
        t_layout.setSpacing(0)

        title_lbl = QLabel(f"  Эмулятор - [{self.username}@{self.hostname}]")
        title_lbl.setObjectName("TitleText")
        t_layout.addWidget(title_lbl)

        title_bar.mousePressEvent = self.start_drag
        title_lbl.mousePressEvent = self.start_drag

        self.add_control_buttons(t_layout)
        layout.addWidget(title_bar)

    def add_control_buttons(self, layout: QHBoxLayout):
        """Добавление кнопок управления окном."""
        btn_container = QWidget()
        btn_layout = QHBoxLayout(btn_container)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setSpacing(2)

        btn_layout.addWidget(self.make_btn(self.draw_icon("min"), self.showMinimized))
        btn_layout.addWidget(self.make_btn(self.draw_icon("max"), self.toggle_maximize))
        btn_layout.addWidget(self.make_btn(self.draw_icon("close"), self.close))

        layout.addWidget(btn_container, alignment=Qt.AlignmentFlag.AlignRight)

    def make_btn(self, icon: QIcon, slot) -> QPushButton:
        """Фабрика для создания кнопок."""
        btn = QPushButton()
        btn.setObjectName("WinBtn")
        btn.setFixedSize(16, 14)
        btn.setIcon(icon)
        btn.setIconSize(QSize(16, 14))
        btn.clicked.connect(slot)
        return btn

    def draw_icon(self, mode: str) -> QIcon:
        """Отрисовка инок с кэшированием."""
        if mode in self._icon_cache:
            return self._icon_cache[mode]

        pixmap = QPixmap(16, 16)
        pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(pixmap)
        pen = QPen(Qt.GlobalColor.black, 1, Qt.PenStyle.SolidLine)
        painter.setPen(pen)

        if mode == "min":
            painter.drawLine(3, 11, 8, 11)
        elif mode == "max":
            painter.drawRect(3, 4, 9, 7)
            painter.drawLine(3, 5, 12, 5)
        elif mode == "close":
            painter.drawLine(4, 4, 10, 10)
            painter.drawLine(5, 4, 11, 10)
            painter.drawLine(4, 10, 10, 4)
            painter.drawLine(5, 10, 11, 4)
        elif mode == "arrow_up":
            painter.setBrush(QBrush(Qt.GlobalColor.black))
            points = [QPoint(8, 5), QPoint(3, 11), QPoint(13, 11)]
            painter.drawPolygon(points)
        elif mode == "arrow_down":
            painter.setBrush(QBrush(Qt.GlobalColor.black))
            points = [QPoint(8, 11), QPoint(3, 5), QPoint(13, 5)]
            painter.drawPolygon(points)

        painter.end()
        icon = QIcon(pixmap)
        self._icon_cache[mode] = icon
        return icon

    def create_two_level_input_zone(self, layout: QVBoxLayout):
        """Создание нижней панели ввода."""
        input_container = QVBoxLayout()
        input_container.setSpacing(4)

        self.prompt_label = QLabel()
        self.prompt_label.setObjectName("PromptLabel")
        self.prompt_label.setFixedHeight(20)
        input_container.addWidget(self.prompt_label)

        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(4)

        self.input_field = QLineEdit()
        self.input_field.returnPressed.connect(self.handle_input)
        bottom_row.addWidget(self.input_field)

        run_btn = QPushButton("Send")
        run_btn.setObjectName("RunBtn")
        run_btn.setFixedSize(50, 22)
        run_btn.clicked.connect(self.handle_input)
        bottom_row.addWidget(run_btn)

        input_container.addLayout(bottom_row)
        layout.addLayout(input_container)

    def _get_formatted_pwd(self) -> str:
        """Форматирование пути текущей директории."""
        pwd = self.interpreter.vfs.get_pwd()
        return pwd.replace("/home", "~", 1) if pwd.startswith("/home") else pwd

    def update_prompt_label(self):
        """Обновление текста приглашения."""
        display_path = self._get_formatted_pwd()
        self.prompt_label.setText(f"{self.username}@{self.hostname}:{display_path}")

    def run_startup_script(self, config_manager):
        """Исполнение стартового скрипта с отображением ввода и вывода."""
        self.output_area.append(config_manager.get_debug_info())
        script_path = config_manager.script_path

        if not script_path or not os.path.exists(script_path):
            return

        try:
            with open(script_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except OSError:
            return

        for line in lines:
            raw_line = line.strip()
            if not raw_line or raw_line.startswith("#"):
                continue

            pwd = self._get_formatted_pwd()
            log_prompt = f"{self.username}@{self.hostname}:{pwd}$ "
            self.output_area.append(f"{log_prompt}{raw_line}")

            res, should_exit, should_clear = self.interpreter.execute(raw_line)
            if should_clear:
                self.output_area.clear()
            elif res:
                self.output_area.append(res)

            if should_exit:
                self.close()
                break
            self.update_prompt_label()

    def toggle_maximize(self):
        """Переключение полноэкранного режима."""
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def start_drag(self, event):
        """Перемещение окна."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.windowHandle().startSystemMove()
            event.accept()

    def handle_input(self):
        """Обработка ввода пользователя."""
        text = self.input_field.text().strip()
        if not text:
            return

        pwd = self._get_formatted_pwd()
        log_prompt = f"{self.username}@{self.hostname}:{pwd}$ "
        self.output_area.append(f"{log_prompt}{text}")

        response, should_exit, should_clear = self.interpreter.execute(text)

        if should_clear:
            self.output_area.clear()
        elif response:
            self.output_area.append(response)

        self.input_field.clear()
        self.update_prompt_label()

        if should_exit:
            self.close()
