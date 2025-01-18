import sys

from PySide6.QtCore import QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView
from app.ui.ui import Ui_MainWindow 
from app.ui.wallet_item_ui import Ui_MyWidget
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject,QUrl, Signal, Slot, Qt)
import asyncio
from app.managers.solana_manager import SolanaManager
import asyncio
from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QTextCursor
from app.dataclases.utils import *
from app.managers.wallet_managers import wallet
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox, QWidget
from app.utils.converter import *
from qasync import QEventLoop
from app.utils.parser_form import *
from app.dataclases.tokensData import useTokenInfo

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
        self.update_button.clicked.connect(lambda: asyncio.create_task(solana_manager.update()))
        
        
        # Настройка перенаправления вывода
        self.console_output = ConsoleOutput()
        self.console_output.text_written.connect(self.update_console)

        # Устанавливаем перенаправление вывода
        sys.stdout = self.console_output
        sys.stderr = self.console_output
        
        self.populate_wallets()
        
    
    @Slot()
    def populate_wallets(self):
        """
        Обновляет виджеты кошельков, добавляя новые и удаляя устаревшие.
        """
        # Получить текущие виджеты
        current_wallets = {self.scroll_Wallets.itemAt(i).widget().wallet_instance for i in range(self.scroll_Wallets.count())}

        # Получить новые кошельки
        new_wallets = {useClass for useClass in self.solana_manager.wallets}

        # Удалить устаревшие виджеты
        for wallet in current_wallets - new_wallets:
            for i in range(self.scroll_Wallets.count()):
                item = self.scroll_Wallets.itemAt(i)
                if item.widget().wallet_instance == wallet:
                    item.widget().deleteLater()
                    self.scroll_Wallets.removeItem(item)
                    break

        # Добавить новые виджеты
        for wallet in new_wallets - current_wallets:
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
                await self.solana_manager.buy_token( amount,self.show_confirmation_dialog)
        except Exception:
            print("НЕВОЗМОЖНО ПРОИЗВЕСТИ ОПЕРАЦИЮ")


    @Slot()
    async def sell_token(self):
        text = self.sell_input.text()
        amount=parsing_number(text,-1)
        lamp=amount_to_token_units(amount,self.solana_manager.decimals) if amount!=-1 else -1
        await self.solana_manager.sell_token(lamp, self.show_confirmation_dialog)
        # except Exception:
        #     print("НЕВОЗМОЖНО ПРОИЗВЕСТИ ОПЕРАЦИЮ")
        

    async def show_confirmation_dialog(self, message: str):
        # Create the QMessageBox
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setText(message)
        msg_box.setWindowTitle('Confirmation')

        # Add custom buttons
        continue_button = msg_box.addButton('Продолжить', QMessageBox.YesRole)
        stop_button = msg_box.addButton('Прекратить', QMessageBox.NoRole)
        
        

        # Show the message box and wait for user interaction
        msg_box.exec_()

        # Determine which button was clicked
        clicked_button = msg_box.clickedButton()

        if clicked_button == continue_button:
            return False
        elif clicked_button == stop_button:
            return True

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
    def __init__(self, solana_manager: SolanaManager, parent: MainWindow = None):
        super(MyWidget, self).__init__(parent)
        self.setupUi(self)
        self.wallet_instance: UseClasses = None
        self.solana_manager = solana_manager
        self.parentMain = parent

        self.is_master_button.clicked.connect(lambda: asyncio.create_task(self.toggle_master_wallet()))
        self.delete_button.clicked.connect(lambda: asyncio.create_task(self.delete_wallet()))
        self.use.stateChanged.connect(lambda state: asyncio.create_task(self.on_use_state_changed(state)))
        self.priority.editingFinished.connect(self.on_priority_changed)

    @Slot(UseClasses)
    def view(self, useClass: UseClasses):
        self.wallet_instance = useClass

        # # Настройка начального состояния
        self.use.setChecked(self.wallet_instance.is_use)
        self.is_master_button.setText("MASTER" if self.wallet_instance.wallet.is_master else "SIMPLE")
        self.name.setText(self.wallet_instance.wallet.name)
        self.adress.setText(str(self.wallet_instance.wallet.get_public_key()))
        self.balance_sol.setText(str(lamports_to_sol(self.wallet_instance.wallet.balance)))

        if self.wallet_instance.wallet.use_token_balance is not None:
            token_balance:useTokenInfo = self.wallet_instance.wallet.use_token_balance
            amount = str(token_units_to_amount(token_balance.tokenInfo.token_amount.amount, self.solana_manager.decimals))
            if token_balance.confirmation:
                self.balance_use.setStyleSheet("border: none; border-bottom: 2px solid green;")
            else:
                self.balance_use.setStyleSheet("border: none; border-bottom: 2px solid yellow;")
            self.balance_use.setText(amount)
        else:
            self.balance_use.setStyleSheet("border: none;")
            self.balance_use.setText("-")

        self.priority.setText(str(lamports_to_sol(self.wallet_instance.usepriorityLevelWithMaxLamports)))

        # Подключение сигналов
        self.wallet_instance.is_use_changed.connect(self.update_use_display)
        self.wallet_instance.usepriorityLevelWithMaxLamports_changed.connect(self.update_priority_display)

        self.wallet_instance.wallet.balanceChanged.connect(self.update_balance_display)
        
        self.wallet_instance.wallet.useTokenBalanceChanged.connect(self.update_useTokenBalance_display)


    async def on_use_state_changed(self, state):
        if self.wallet_instance:
            self.wallet_instance.is_use = state == 2
            await self.solana_manager.init_wallets()

    def on_priority_changed(self):
        if self.wallet_instance:
            try:
                value = sol_to_lamports(float(self.priority.text()))
                self.wallet_instance.usepriorityLevelWithMaxLamports = value
            except ValueError:
                # Неверный ввод, игнорируем
                pass

    async def toggle_master_wallet(self):
        if self.wallet_instance:
            is_master = self.is_master_button.text() == "SIMPLE"
            await self.solana_manager.set_master_wallet(self.wallet_instance.wallet, is_master)
            self.is_master_button.setText("MASTER" if is_master else "SIMPLE")
            self.wallet_instance.wallet.is_master = is_master

    async def delete_wallet(self):
        if self.wallet_instance:
            if await self.solana_manager.delete_wallet(self.wallet_instance.wallet):
                self.parentMain.populate_wallets()

    def update_use_display(self, value: bool):
        self.use.setChecked(value)

    def update_priority_display(self, value: int):
        self.priority.setText(str(lamports_to_sol(value)))


    def update_master_display(self, value: bool):
        self.is_master_button.setText("MASTER" if value else "SIMPLE")

    def update_balance_display(self, value: int):
        self.balance_sol.setText(str(lamports_to_sol(value)))

    def update_useTokenBalance_display(self,value: useTokenInfo):
        if value is not None:
            token_balance:useTokenInfo = value
            amount = str(token_units_to_amount(token_balance.tokenInfo.token_amount.amount, self.solana_manager.decimals))
            if token_balance.confirmation:
                self.balance_use.setStyleSheet("border: none; border-bottom: 2px solid green;")
            else:
                self.balance_use.setStyleSheet("border: none; border-bottom: 2px solid yellow;")
            self.balance_use.setText(amount)
        else:
            self.balance_use.setStyleSheet("border: none;")
            self.balance_use.setText("-")

    

