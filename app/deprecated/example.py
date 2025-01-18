from PySide6.QtCore import Qt, QTimer, QRectF
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from PySide6.QtGui import QPainter, QColor


class CircularLoader(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(100, 100)  # Размер круга
        self.angle = 0  # Начальный угол анимации

        # Таймер для анимации
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)

    def start(self):
        self.timer.start(16)  # Запускаем анимацию (~60 FPS)

    def stop(self):
        self.timer.stop()  # Останавливаем анимацию

    def update_animation(self):
        self.angle = (self.angle + 5) % 360
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = QRectF(10, 10, self.width() - 20, self.height() - 20)
        start_angle = self.angle * 16
        span_angle = 120 * 16

        # Настройка пера
        pen_color = QColor(66, 135, 245)
        pen_width = 8
        pen = painter.pen()
        pen.setColor(pen_color)
        pen.setWidth(pen_width)
        painter.setPen(pen)

        # Рисуем дугу
        painter.drawArc(rect, start_angle, span_angle)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Button with Loader")
        self.setFixedSize(300, 200)

        # Основной макет
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        # Кнопка
        self.button = QPushButton("Click Me", self)
        self.button.setFixedSize(120, 50)
        self.button.clicked.connect(self.show_loader)
        layout.addWidget(self.button)

        # Индикатор загрузки
        self.loader = CircularLoader(self)
        self.loader.hide()  # Скрываем по умолчанию
        layout.addWidget(self.loader)

    def show_loader(self):
        # Скрыть кнопку и показать загрузку
        self.button.hide()
        self.loader.show()
        self.loader.start()

        # Имитация завершения работы (через 3 секунды)
        QTimer.singleShot(3000, self.hide_loader)

    def hide_loader(self):
        # Остановить загрузку и вернуть кнопку
        self.loader.stop()
        self.loader.hide()
        self.button.show()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()