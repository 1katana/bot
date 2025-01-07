import sys

from PySide6.QtCore import QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView
from ui import Ui_MainWindow 
from wallet_item_ui import Ui_MyWidget
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QHBoxLayout, QLineEdit,
    QSizePolicy, QToolButton, QWidget, QVBoxLayout, QScrollArea)
import asyncio
from solana_manager import SolanaManager
from PySide6.QtWidgets import QPlainTextEdit
from PySide6.QtCore import QThread, Signal, Slot
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
import asyncio
from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QTextCursor

class Worker(QThread):
    result = Signal(str)

    def __init__(self, solana_manager, task, *args, **kwargs):
        super().__init__()
        self.solana_manager = solana_manager
        self.task = task
        self.args = args
        self.kwargs = kwargs

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.async_run())

    async def async_run(self):
        result = await self.task(*self.args, **self.kwargs)
        self.result.emit(result)



class MyWidget(QWidget, Ui_MyWidget):
    def __init__(self, parent=None):
        super(MyWidget, self).__init__(parent)
        self.setupUi(self)


class ConsoleOutput(QObject):
    text_written = Signal(str)

    def write(self, text):
        self.text_written.emit(str(text))

    def flush(self):
        pass  # Этот метод можно оставить пустым



class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, solana_manager):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.solana_manager = solana_manager

        self.webEngineView.setUrl(QUrl("https://solscan.io/"))

        # Connect buttons to functions
        self.add_wallet_button.clicked.connect(self.add_wallet)
        self.raspr_button.clicked.connect(self.distribute_funds)
        self.sobr_button.clicked.connect(self.collect_funds)
        self.create_wallets.clicked.connect(self.create_wallets_fun)
        self.load_direct.clicked.connect(self.load_from_dir)
        self.use_token_adress.clicked.connect(self.use_token)
        self.buy_button.clicked.connect(self.buy_token)
        self.sell_button.clicked.connect(self.sell_token)
        
        # Настройка перенаправления вывода
        self.console_output = ConsoleOutput()
        self.console_output.text_written.connect(self.update_console)

        # Устанавливаем перенаправление вывода
        sys.stdout = self.console_output
        sys.stderr = self.console_output
        
        
        for i in range(10):
            widget = MyWidget(self)
            widget.name.setText(f"Wallet{i}")
            widget.adress.setText(f"Address {i}тлцдлукмтдлукмтлукмтлукмтукдлмлуктммук")
            widget.balance_sol.setText(f"0.12344")
            widget.balance_use.setText(f"133344.02121")
            widget.priority.setText(f"0.04")
            self.scroll_Wallets.addWidget(widget)  # Используйте addWidget

    @Slot()
    def add_wallet(self):
        secret_key = self.input_secret.text()
        self.start_task(self.solana_manager.add_wallet, secret_key)

    @Slot()
    def distribute_funds(self):
        self.start_task(self.solana_manager.distribute_funds)

    @Slot()
    def collect_funds(self):
        self.start_task(self.solana_manager.collect_funds_to_master)

    @Slot()
    def create_wallets_fun(self):
        num_wallets = self.spinBox.value()
        self.start_task(self.solana_manager.create_wallets, num_wallets)

    @Slot()
    def load_from_dir(self):
        self.start_task(self.solana_manager.load_from_dir)

    @Slot()
    def use_token(self):
        token_address = self.token_adress.text()
        self.start_task(self.solana_manager.use_token, token_address)

    @Slot()
    def buy_token(self):
        amount = int(self.buy_sol_input.text())
        self.start_task(self.solana_manager.buy_token, amount, self.confirmation_callback)

    @Slot()
    def sell_token(self):
        amount = int(self.sell_input.text())
        self.start_task(self.solana_manager.sell_token, self.confirmation_callback, amount)

    def start_task(self, task, *args, **kwargs):
        self.worker = Worker(self.solana_manager, task, *args, **kwargs)
        self.worker.result.connect(self.update_console)
        self.worker.start()

    @Slot(str)
    def update_console(self, message):
        self.console.appendPlainText(message)
        
    @Slot(str)
    def update_console(self, text):
        # Добавление текста в QPlainTextEdit
        self.console.moveCursor(QTextCursor.End)  # Перемещаем курсор в конец
        self.console.insertPlainText(text)
        self.console.ensureCursorVisible()  # Делаем видимой текущую позицию курсора

    async def confirmation_callback(self, message: str) -> bool:
        user_input = input(f"{message} (y/n): ").strip().lower()
        return user_input in {"y", "yes"}


async def main():
    app = QApplication([])
    solana_manager = await SolanaManager.create()
    window = MainWindow(solana_manager)
    window.show()
    app.exec()

if __name__ == "__main__":
    asyncio.run(main())