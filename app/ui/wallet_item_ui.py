from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject,QUrl, Signal, Slot, Qt)
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QApplication, QVBoxLayout, QMainWindow, QPushButton, QMessageBox, QWidget
from app.ui.design.setting import Ui_Form
from app.managers.config import Config
from app.utils.converter import *
from app.utils.parser_form import *
from app.managers.solana_manager import SolanaManager
# from app.ui.main_ui import MainWindow
from app.dataclases.utils import UseClasses
from app.dataclases.tokensData import useTokenInfo
from app.ui.design.wallet_item_ui import Ui_MyWidget
import asyncio

class Wallet_item_ui(QWidget, Ui_MyWidget):
    def __init__(self, solana_manager: SolanaManager, parent = None):
        super(Wallet_item_ui, self).__init__(parent)
        self.setupUi(self)
        self.wallet_instance: UseClasses = None
        self.solana_manager = solana_manager
        self.parentMain = parent
    

        self.is_master_button.clicked.connect(lambda: asyncio.create_task(self.toggle_master_wallet()))
        self.delete_button.clicked.connect(lambda: asyncio.create_task(self.delete_wallet()))
        self.use.stateChanged.connect(lambda state: asyncio.create_task(self.on_use_state_changed(state)))
        
        
        layout = self.layout()  
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

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

        # Подключение сигналов
        self.wallet_instance.is_use_changed.connect(self.update_use_display)

        self.wallet_instance.wallet.balanceChanged.connect(self.update_balance_display)
        
        self.wallet_instance.wallet.useTokenBalanceChanged.connect(self.update_useTokenBalance_display)


    async def on_use_state_changed(self, state):
        if self.wallet_instance:
            self.wallet_instance.is_use = state == 2
            await self.solana_manager.init_wallets()


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

    

