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
from dataclases.utils import UseClases
from wallet import Wallet
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox
from functools import partial

class Worker(QThread):
    result = Signal(str)
    confirmation_requested = Signal(str)
    confirmation_result = Signal(bool)

    def __init__(self, solana_manager, task, *args, **kwargs):
        super().__init__()

        # Извлекаем use_callback из kwargs
        use_callback = kwargs.pop('use_callback', False)
        
        # Пропускаем callable аргументы, если они присутствуют
        args = [arg for arg in args if not callable(arg)]
        
        # Сохраняем параметры
        self.solana_manager = solana_manager
        self.task = task
        self.args = args
        self.kwargs = kwargs
        
        # Если требуется callback, подключаем его и передаем в task
        if use_callback:
            # Подключаем сигнал для обработки подтверждения
            self.confirmation_requested.connect(self.confirmation_callback)

            self.args.append(self.confirmation_callback)
        
    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.async_run())

    async def async_run(self):
        # Выполнение асинхронной задачи
        print("Executing task with args:", self.args, "kwargs:", self.kwargs)

        result = await self.task(*self.args, **self.kwargs)
        self.result.emit(result)


    def confirmation_callback(self, message: str):
        # Эмулируем запрос на подтверждение с использованием GUI
        self.confirmation_requested.emit(message)




class ConsoleOutput(QObject):
    text_written = Signal(str)

    def write(self, text):
        self.text_written.emit(str(text))

    def flush(self):
        pass  # Этот метод можно оставить пустым



class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, solana_manager:SolanaManager):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.solana_manager = solana_manager
        
        self.BASE_URL="https://solscan.io/"

        self.webEngineView.setUrl(QUrl(self.BASE_URL))

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
        
        self.populate_wallets()
        
    
    @Slot()
    def populate_wallets(self):
        # Очистить текущие виджеты
        while self.scroll_Wallets.count():
            item = self.scroll_Wallets.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Добавить новые виджеты для каждого кошелька
        for wallet in self.solana_manager.wallets:
            widget = MyWidget(solana_manager=self.solana_manager, start_task=self.start_task, parent=self)
            widget.view(wallet)
            self.scroll_Wallets.addWidget(widget)
            
    


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
        self.start_task(self.solana_manager.set_use_token, token_address)
        self.webEngineView.setUrl(QUrl(self.BASE_URL+"/token/"+token_address))

    @Slot()
    def buy_token(self):
        amount = int(self.buy_sol_input.text())
        self.start_task(self.solana_manager.buy_token, amount, use_callback=True)


    @Slot()
    def sell_token(self):
        amount = int(self.sell_input.text())
        self.start_task(self.solana_manager.sell_token,amount, use_callback=True)


    # def start_task(self, task, *args, **kwargs):
    #     self.worker = Worker(self.solana_manager, task, *args, **kwargs)
    #     self.worker.result.connect(self.update_console)
    #     self.worker.result.connect(self.populate_wallets)
    #     self.worker.start()
    
    def show_confirmation_dialog(self, message: str):
        # Вызов подтверждения через QMessageBox в главном потоке
        reply = QMessageBox.question(self, 'Confirmation', message,
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        self.worker.confirmation_result.emit(reply == QMessageBox.Yes)

    def handle_confirmation_result(self, confirmed: bool):
        if confirmed:
            print("Пользователь подтвердил действие.")
        else:
            print("Пользователь отменил действие.")
        
    def start_task(self, task, *args, **kwargs):
        
        # Создаем объект Worker
        self.worker = Worker(self.solana_manager, task, *args, **kwargs)
        self.worker.result.connect(self.update_console)
        self.worker.result.connect(self.populate_wallets)
        self.worker.confirmation_requested.connect(self.show_confirmation_dialog)

        self.worker.start()

    @Slot(bool)
    def handle_confirmation_result(self, confirmed: bool):
        if confirmed:
            print("User confirmed the action.")
            # Продолжить выполнение задачи
        else:
            print("User canceled the action.")
            # Отменить выполнение задачи

    @Slot(str)
    def update_console(self, message):
        self.console.appendPlainText(message)
        
    @Slot(str)
    def update_console(self, text):
        # Добавление текста в QPlainTextEdit
        self.console.moveCursor(QTextCursor.End)  # Перемещаем курсор в конец
        self.console.insertPlainText(text)
        self.console.ensureCursorVisible()  # Делаем видимой текущую позицию курсора




class MyWidget(QWidget, Ui_MyWidget):
    def __init__(self,solana_manager:SolanaManager,start_task, parent:MainWindow =None):
        super(MyWidget, self).__init__(parent)
        self.setupUi(self)
        self.wallet_instance = None
        self.solana_manager=solana_manager
        self.start_task=start_task

        self.parentMain=parent
        
        
        self.is_master_button.clicked.connect(self.toggle_master_wallet)
        self.delete_button.clicked.connect(self.delete_wallet)
    
    @Slot(UseClases)
    def view(self, wallet: UseClases):
        self.wallet_instance = wallet
        self.use.setChecked(wallet.is_use)
        self.is_master_button.setText("MASTER" if wallet.wallet.is_master else "SIMPLE")
        self.name.setText(wallet.wallet.name)
        self.adress.setText(str(wallet.wallet.get_public_key()))
        self.balance_sol.setText(str(wallet.wallet.balance))
        self.balance_use.setText("НЕ МОГУ")
        self.priority.setText(str(wallet.usepriorityLevelWithMaxLamports))
        
                # Подключите сигналы к слотам
        wallet.is_use_changed.connect(self.update_use_display)
        wallet.usepriorityLevelWithMaxLamports_changed.connect(self.update_priority_display)

        self.use.stateChanged.connect(self.update_use)
        self.priority.textChanged.connect(self.update_priority)

    
    def update_use(self, state):
        if self.wallet_instance:
            self.wallet_instance.is_use = state == 2  # 2 соответствует состоянию "включено"
            self.start_task(self.solana_manager.init_wallets)
            

    def toggle_master_wallet(self):
        if self.wallet_instance:
            is_master = self.is_master_button.text() == "SIMPLE"
            self.start_task(self.solana_manager.set_master_wallet,self.wallet_instance.wallet, is_master)
            self.parentMain.populate_wallets()
            
    def delete_wallet(self):
        if self.wallet_instance:
            self.start_task(self.solana_manager.delete_wallet,self.wallet_instance.wallet)
            
    @Slot(str)
    def update_priority(self, text):
        if self.wallet_instance:
            try:
                value = int(text)
                self.wallet_instance.usepriorityLevelWithMaxLamports = value
            except ValueError:
                # Обработка некорректного ввода, если необходимо
                pass

    def update_use_display(self, value):
        self.use.setChecked(value)

    def update_priority_display(self, value):
        self.priority.setText(str(value))






async def main():
    app = QApplication([])
    solana_manager = await SolanaManager.create()
    window = MainWindow(solana_manager)
    window.show()
    app.exec()

if __name__ == "__main__":
    asyncio.run(main())
    