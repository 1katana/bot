import sys

from PySide6.QtCore import QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView
from ui import Ui_MainWindow 
from wallet_item_ui import Ui_MyWidget
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject,QUrl, Qt)
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
from converter import *

from qasync import QEventLoop


def parsing_number(text: str,default):
    text=text.replace(" ","")
    if text=="":
        return default
    else:
        try:
            return float(text)
        except ValueError:
            print(f"{text} - НЕ ЧИСЛО")




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
        self.add_wallet_button.clicked.connect(lambda: asyncio.create_task(self.add_wallet()))
        self.raspr_button.clicked.connect(lambda: asyncio.create_task(self.distribute_funds()))
        self.sobr_button.clicked.connect(lambda: asyncio.create_task(self.collect_funds()))
        self.create_wallets.clicked.connect(lambda: asyncio.create_task(self.create_wallets_fun()))
        self.load_direct.clicked.connect(lambda: asyncio.create_task(self.load_from_dir()))
        self.use_token_adress.clicked.connect(lambda: asyncio.create_task(self.use_token()))
        self.buy_button.clicked.connect(lambda: asyncio.create_task(self.buy_token()))
        self.sell_button.clicked.connect(lambda: asyncio.create_task(self.sell_token()))
        
        
        
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
            widget = MyWidget(solana_manager=self.solana_manager, parent=self)
            widget.view(wallet)
            self.scroll_Wallets.addWidget(widget)
            
    


    @Slot()
    async def add_wallet(self):
        secret_key = self.input_secret.text()
        # self.start_task(self.solana_manager.add_wallet, secret_key)
        await self.solana_manager.add_wallet(secret_key)
        self.populate_wallets()

    @Slot()
    async def distribute_funds(self):
        text=self.buy_sol_input.text()
        
        try:
            amount=parsing_number(text,-1)
            if amount !=-1:
                amount=sol_to_lamports(amount)
            await self.solana_manager.distribute_funds(amount)
        except Exception:
            print("НЕВОЗМОЖНО ПРОИЗВЕСТИ ОПЕРАЦИЮ")

    @Slot()
    async def collect_funds(self):
        await self.solana_manager.collect_funds_to_master()


    @Slot()
    async def create_wallets_fun(self):
        num_wallets = self.spinBox.value()
        await self.solana_manager.create_wallets(num_wallets)
        self.populate_wallets()

    @Slot()
    async def load_from_dir(self):
        await self.solana_manager.load_from_dir()
        self.populate_wallets()

    @Slot()
    async def use_token(self):
        token_address = self.token_adress.text().replace(" ","")
        if token_address=="":
            print("ВВЕДИТЕ ТОКЕН!!!")
        await self.solana_manager.set_use_token(token_address)
        print(self.solana_manager.use_token)
        self.webEngineView.setUrl(QUrl(self.BASE_URL+"/token/"+token_address))

    @Slot()
    async def buy_token(self):
        text = self.buy_sol_input.text()
        try:
            amount=parsing_number(text,0)
            if amount !=0:
                amount=sol_to_lamports(amount)
                await self.solana_manager.buy_token( amount,self.confirmation_callback)
        except Exception:
            print("НЕВОЗМОЖНО ПРОИЗВЕСТИ ОПЕРАЦИЮ")


    @Slot()
    async def sell_token(self):
        text = self.sell_input.text()
        try:
            amount=int(parsing_number(text,-1))
            await self.solana_manager.sell_token(amount, self.show_confirmation_dialog)
        except Exception:
            print("НЕВОЗМОЖНО ПРОИЗВЕСТИ ОПЕРАЦИЮ")
        

    async def show_confirmation_dialog(self, message: str):
        # Create the QMessageBox
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setText(message)
        msg_box.setWindowTitle('Confirmation')

        # Add custom buttons
        stop_button = msg_box.addButton('Продолжить', QMessageBox.NoRole)
        continue_button = msg_box.addButton('Прекратить', QMessageBox.YesRole)
        

        # Show the message box and wait for user interaction
        msg_box.exec_()

        # Determine which button was clicked
        clicked_button = msg_box.clickedButton()

        if clicked_button == continue_button:
            return True
        elif clicked_button == stop_button:
            return False

    # @Slot(str)
    # def update_console(self, message):
    #     self.console.appendPlainText(message)
        
    @Slot(str)
    def update_console(self, text):
        # Добавление текста в QPlainTextEdit
        self.console.moveCursor(QTextCursor.End)  # Перемещаем курсор в конец
        self.console.insertPlainText(text)
        self.console.ensureCursorVisible()  # Делаем видимой текущую позицию курсора

    async def confirmation_callback(self, message: str) -> bool:
        user_input = input(f"{message} (y/n): ").strip().lower()
        return user_input in {"y", "yes"}




class MyWidget(QWidget, Ui_MyWidget):
    def __init__(self,solana_manager:SolanaManager, parent:MainWindow =None):
        super(MyWidget, self).__init__(parent)
        self.setupUi(self)
        self.wallet_instance = None
        self.solana_manager=solana_manager

        self.parentMain=parent
        
        
        self.is_master_button.clicked.connect(lambda: asyncio.create_task(self.toggle_master_wallet()))
        self.delete_button.clicked.connect(lambda: asyncio.create_task(self.delete_wallet()))
    
    @Slot(UseClases)
    def view(self, wallet: UseClases):
        self.wallet_instance = wallet
        self.use.setChecked(wallet.is_use)
        self.is_master_button.setText("MASTER" if wallet.wallet.is_master else "SIMPLE")
        self.name.setText(wallet.wallet.name)
        self.adress.setText(str(wallet.wallet.get_public_key()))
        self.balance_sol.setText(str(lamports_to_sol(wallet.wallet.balance)))
        self.balance_use.setText("НЕ МОГУ")
        self.priority.setText(str(lamports_to_sol(wallet.usepriorityLevelWithMaxLamports)))
        
                # Подключите сигналы к слотам
        wallet.is_use_changed.connect(self.update_use_display)
        # wallet.usepriorityLevelWithMaxLamports_changed.connect(self.update_priority_display)

        self.use.stateChanged.connect(lambda: asyncio.create_task(self.update_use()))
        
        self.priority.textChanged.connect(self.update_priority)

    
    async def update_use(self, state):
        if self.wallet_instance:
            self.wallet_instance.is_use = state == 2  # 2 соответствует состоянию "включено"
            await self.solana_manager.init_wallets()
            

    async def toggle_master_wallet(self):
        if self.wallet_instance:
            is_master = self.is_master_button.text() == "SIMPLE"
            await self.solana_manager.set_master_wallet(self.wallet_instance.wallet, is_master)
            self.parentMain.populate_wallets()
            
    async def delete_wallet(self):
        if self.wallet_instance:
            await self.solana_manager.delete_wallet(self.wallet_instance.wallet)
            self.parentMain.populate_wallets()
            
    @Slot(str)
    def update_priority(self, text):
        if self.wallet_instance:
            try:
                value=parsing_number(text,4000000/1_000_000_000)
                
                lamports=sol_to_lamports(value)
                
                self.wallet_instance.usepriorityLevelWithMaxLamports = lamports
                self.priority.setText(str(lamports))
            except ValueError:
                # Обработка некорректного ввода, если необходимо
                pass

    def update_use_display(self, value):
        self.use.setChecked(value)

    # def update_priority_display(self, value):
    #     self.priority.setText(str(value))
        
    






async def main():
    solana_manager = await SolanaManager.create()

    app = QApplication([])
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    window = MainWindow(solana_manager)
    window.show()
    
    with loop:
        await loop.run_forever()
        if window.close():
            loop.close()

if __name__ == "__main__":
    asyncio.run(main())
    