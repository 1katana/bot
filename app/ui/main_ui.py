import sys

from PySide6.QtCore import QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView
from app.ui.design.ui import Ui_MainWindow 
from app.ui.design.wallet_item_ui import Ui_MyWidget
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject,QUrl, Signal, Slot, Qt)
import asyncio
from app.managers.solana_manager import SolanaManager
import asyncio
from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QTextCursor
from app.dataclases.utils import *
from app.managers.wallet_managers import wallet
from PySide6.QtWidgets import QApplication, QVBoxLayout, QMainWindow, QPushButton, QMessageBox, QWidget
from app.utils.converter import *
from qasync import QEventLoop
from app.utils.parser_form import *
from app.dataclases.tokensData import useTokenInfo
from app.ui.design.setting import Ui_Form
from app.managers.config import Config
from app.ui.setting_ui import *
from app.ui.wallet_item_ui import Wallet_item_ui
from app.ui.create_token_ui import *

class ConsoleOutput(QObject):
    text_written = Signal(str)

    def write(self, text):
        self.text_written.emit(str(text))

    def flush(self):
        pass  # Этот метод можно оставить пустым



class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, solana_manager: SolanaManager):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.solana_manager = solana_manager

        # self.BASE_URL = "https://solscan.io/"
        
        
        self.token_creation_is_open = TokenCreationState()
        self.settings_is_open = SettingsState()
        
        self.show_creating_token()
        
        
        
        self.solana_manager.pumpFunTokenCreator.validMetadataChanged.connect(self.show_creating_token)
        
        self.toolButton.clicked.connect(self.show_setting_window)
        self.add_wallet_button.clicked.connect(lambda: asyncio.create_task(self.add_wallet()))
        self.raspr_button.clicked.connect(lambda: asyncio.create_task(self.distribute_funds()))
        self.sobr_button.clicked.connect(lambda: asyncio.create_task(self.collect_funds()))
        self.create_wallets.clicked.connect(lambda: asyncio.create_task(self.create_wallets_fun()))
        self.load_direct.clicked.connect(lambda: asyncio.create_task(self.load_from_dir()))
        self.use_token_adress.clicked.connect(lambda: asyncio.create_task(self.use_token()))
        self.buy_button.clicked.connect(lambda: asyncio.create_task(self.buy_token()))
        self.sell_button.clicked.connect(lambda: asyncio.create_task(self.sell_token()))
        self.update_button.clicked.connect(lambda: asyncio.create_task(solana_manager.update()))
        self.form_create_token.clicked.connect(self.show_token_create_form)
        
        self.solana_manager.use_token_changed.connect(self.update_use_token)
        self.update_use_token()
        # if solana_manager.use_token is not None:
        #     self.token_adress.setText(solana_manager.use_token)
        #     self.webEngineView.setUrl(QUrl(self.BASE_URL + "token/" + solana_manager.use_token))
        #     print(self.BASE_URL + solana_manager.use_token)
        # else:
        #     self.webEngineView.setUrl(QUrl(self.BASE_URL))

        # Настройка перенаправления вывода
        self.console_output = ConsoleOutput()
        self.console_output.text_written.connect(self.update_console)

        # Устанавливаем перенаправление вывода
        sys.stdout = self.console_output
        sys.stderr = self.console_output

        self.populate_wallets()
        
    def update_use_token(self, new_token=0):
        self.token_adress.setText(self.solana_manager.use_token)
        
    def show_creating_token(self):
        if self.solana_manager.pumpFunTokenCreator.valid_metadata:
            if self.solana_manager.pumpFunTokenCreator.token_data["image_path"]:
                image_path = self.solana_manager.pumpFunTokenCreator.token_data["image_path"]
                pixmap = QPixmap(image_path)
                self.label.setPixmap(pixmap.scaled(200, 200))
                self.name_token_label.setText(self.solana_manager.pumpFunTokenCreator.token_data["name"])
                
                self.buy_sol_input.setPlaceholderText(QCoreApplication.translate("MainWindow", u"amount", None))
            
            
        else:
            pixmap = QPixmap("app\\ui\\design\\empty.jpg")      
            self.label.setPixmap(pixmap.scaled(200, 200))
            self.name_token_label.setText("НЕТ Токена")
            self.buy_sol_input.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u0432 sol", None))
        
    def show_token_create_form(self):
        
        if self.token_creation_is_open.is_open() != True:
            TokenCreationForm(self.token_creation_is_open,self.solana_manager.pumpFunTokenCreator).show()
            self.token_creation_is_open.set_open(True)

    def show_setting_window(self):
        if self.settings_is_open.is_open() != True:
            Settings(self.solana_manager.config, self.settings_is_open).show()
            
            self.settings_is_open.set_open(True)
        
    
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
            widget = Wallet_item_ui(solana_manager=self.solana_manager, parent=self)
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
        text=self.input_raspr.text()
        
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
        # self.webEngineView.setUrl(QUrl(self.BASE_URL+"/token/"+token_address))

    @Slot()
    async def buy_token(self):
        text = self.buy_sol_input.text()
        try:
            amount = parsing_number(text, 0)
            valid_metadata = self.solana_manager.pumpFunTokenCreator.valid_metadata is not None
            use_wallets_length = len(self.solana_manager.use_wallets)

            if valid_metadata and (use_wallets_length == 1 or amount != 0):
                create_amount = parsing_number(self.buy_dev.text(), 0)
                time = parsing_number(self.time.text(), None)
                all_sell_check = self.all_sell_check.isChecked()

                await self.solana_manager.create_token(
                    self.show_confirmation_dialog,
                    int(amount) if use_wallets_length > 1 else 0,  
                    create_amount=int(create_amount),
                    all_wallets=all_sell_check,
                    time=time
                )
            elif amount != 0:
                amount = sol_to_lamports(amount)
                await self.solana_manager.buy_bundles_token(amount, self.show_confirmation_dialog)
        except Exception:
            print("НЕВОЗМОЖНО ПРОИЗВЕСТИ ОПЕРАЦИЮ")



    @Slot()
    async def sell_token(self):
        text = self.sell_input.text()
        amount=parsing_number(text,-1)
        lamp=amount_to_token_units(amount,self.solana_manager.decimals) if amount!=-1 else -1
        await self.solana_manager.sell_bundles_token(lamp, self.show_confirmation_dialog)
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



