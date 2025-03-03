from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject,QUrl, Signal, Slot, Qt)
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QApplication, QVBoxLayout, QMainWindow, QPushButton, QMessageBox, QWidget
from app.ui.design.setting import Ui_Form
from app.managers.config import Config
from app.utils.converter import *
from app.utils.parser_form import *
from app.utils.parser_form import parsing_number

class SettingsState(QObject):
    state_changed = Signal(bool)  # Сигнал об изменении состояния

    def __init__(self):
        super().__init__()
        self._is_open = False

    def is_open(self):
        return self._is_open

    def set_open(self, value: bool):
        if self._is_open != value:
            self._is_open = value
            self.state_changed.emit(self._is_open)  # Уведомление об изменении

class Settings(QWidget, Ui_Form):
    closed = Signal()  # Сигнал для уведомления о закрытии окна

    def __init__(self, config: Config, settings_is_open: SettingsState, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        # Запретить изменение размера окна
        self.setFixedSize(self.size())

        self.settings_is_open = settings_is_open
        self.config = config

        self.init_forms()

        # Связь изменений с локальными переменными
        self.sol_mint.textChanged.connect(lambda text: setattr(self, "temp_sol_mint", text))
        self.SOLANA_API.textChanged.connect(lambda text: setattr(self, "temp_api_key", text))
        self.jupiter_url_7.textChanged.connect(lambda text: setattr(self, "temp_jupiter_url", text))
        self.userpriority.textChanged.connect(lambda text: setattr(self, "temp_userpriority", parsing_number(text, 0)))
        self.jitoTipLamports.textChanged.connect(lambda text: setattr(self, "temp_jitoTipLamports", parsing_number(text, 0)))
        self.jito_url.textChanged.connect(lambda text: setattr(self, "temp_jito_url", text))
        self.pump_fun_url.textChanged.connect(lambda text: setattr(self, "temp_pump_fun_url", text))
        self.dynamic_slippage.toggled.connect(lambda state: setattr(self, "temp_dynamic_slippage", state))

        self.wrapUnwrapSol.toggled.connect(lambda state: setattr(self, "temp_wrapUnwrapSol", state))
        self.dynamicCompute.toggled.connect(lambda state: setattr(self, "temp_dynamicCompute", state))

        self.reset.clicked.connect(self.reset_data)

        self.closed.connect(lambda: self.settings_is_open.set_open(False))

    def closeEvent(self, event):
        """
        Обработчик закрытия окна.
        Сохраняет конфигурацию перед закрытием.
        """
        reply = QMessageBox.question(
            self,
            "Confirm Close",
            "Are you sure you want to close the settings?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            # Проверка изменений
            if (
                self.config.sol_mint != self.temp_sol_mint or
                self.config.api_key != self.temp_api_key or
                self.config.jupiter_url != self.temp_jupiter_url or
                self.config.jito_url != self.temp_jito_url or
                self.config.pump_fun_url != self.temp_pump_fun_url or
                self.config.wallets_dir != self.temp_wallet_dir or
                self.config.jitoTipLamports != self.temp_jitoTipLamports or
                self.config.usepriorityLevelWithMaxLamports != self.temp_userpriority or
                self.config.wrapUnwrapSOL != self.temp_wrapUnwrapSol or
                self.config.dynamicComputeUnitLimit != self.temp_dynamicCompute or
                self.config.dynamic_slippage != self.temp_dynamic_slippage
            ):
                # Конвертация jitoTipLamports в SOL
                if self.config.jitoTipLamports == self.temp_jitoTipLamports:
                    self.temp_jitoTipLamports = lamports_to_sol(self.temp_jitoTipLamports)
                    
                if self.config.usepriorityLevelWithMaxLamports == self.temp_userpriority:
                    self.temp_userpriority = lamports_to_sol(self.temp_userpriority)

                # Сохранение изменений из временных переменных в конфиг
                self.config.sol_mint = self.temp_sol_mint
                self.config.api_key = self.temp_api_key
                self.config.jupiter_url = self.temp_jupiter_url
                self.config.jito_url = self.temp_jito_url
                self.config.pump_fun_url = self.temp_pump_fun_url
                self.config.wallets_dir = self.temp_wallet_dir
                self.config.jitoTipLamports = self.temp_jitoTipLamports
                self.config.usepriorityLevelWithMaxLamports = self.temp_userpriority
                self.config.wrapUnwrapSOL = self.temp_wrapUnwrapSol
                self.config.dynamicComputeUnitLimit = self.temp_dynamicCompute
                self.config.dynamic_slippage = self.temp_dynamic_slippage

                self.config.save_config()  # Сохранение конфигурации

        self.closed.emit()  # Сигнал закрытия
        event.accept()  # Закрыть окно

    def init_forms(self):
        # Локальные переменные для предварительных изменений
        self.temp_sol_mint = self.config.sol_mint
        self.temp_api_key = self.config.api_key
        self.temp_jupiter_url = self.config.jupiter_url
        self.temp_jito_url = self.config.jito_url
        self.temp_pump_fun_url = self.config.pump_fun_url
        self.temp_wallet_dir = self.config.wallets_dir
        self.temp_jitoTipLamports = self.config.jitoTipLamports
        self.temp_userpriority = self.config.usepriorityLevelWithMaxLamports
        self.temp_wrapUnwrapSol = self.config.wrapUnwrapSOL
        self.temp_dynamicCompute = self.config.dynamicComputeUnitLimit
        self.temp_dynamic_slippage = self.config.dynamic_slippage

        # Инициализация полей
        self.jitoTipLamports.setText(str(lamports_to_sol(self.temp_jitoTipLamports)))
        self.userpriority.setText(str(lamports_to_sol(self.temp_userpriority)))
        self.SOLANA_API.setText(self.temp_api_key)
        self.jupiter_url_7.setText(self.temp_jupiter_url)
        self.jito_url.setText(self.temp_jito_url)
        self.pump_fun_url.setText(self.temp_pump_fun_url)
        self.sol_mint.setText(self.temp_sol_mint)
        self.wrapUnwrapSol.setChecked(self.temp_wrapUnwrapSol)
        self.dynamicCompute.setChecked(self.temp_dynamicCompute)
        self.dynamic_slippage.setChecked(self.temp_dynamic_slippage)

    def reset_data(self):
        self.config.reset_to_defaults()
        self.init_forms()