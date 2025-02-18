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
        self.api_key.textChanged.connect(lambda text: setattr(self, "temp_api_key", text))
        self.jupiter_url_7.textChanged.connect(lambda text: setattr(self, "temp_jupiter_url", text))
        self.userpriority.textChanged.connect(lambda text: setattr(self, "temp_userpriority", parsing_number(text,0)))
        self.wallet_dir.textChanged.connect(lambda text: setattr(self, "temp_wallet_dir", text))
        self.MIN.textChanged.connect(lambda text: setattr(self, "temp_min_bps", int(text) if text.isdigit() else 0))
        self.MAX.textChanged.connect(lambda text: setattr(self, "temp_max_bps", int(text) if text.isdigit() else 0))

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
            # Сохранение изменений из временных переменных в конфиг
            self.config.sol_mint = self.temp_sol_mint
            self.config.api_key = self.temp_api_key
            self.config.jupiter_url = self.temp_jupiter_url
            if self.config.usepriorityLevelWithMaxLamports != self.temp_userpriority:
                self.config.usepriorityLevelWithMaxLamports = self.temp_userpriority
            self.config.wallets_dir = self.temp_wallet_dir
            self.config.dynamic_slippage_min = self.temp_min_bps
            self.config.dynamic_slippage_max = self.temp_max_bps
            self.config.wrapUnwrapSOL = self.temp_wrapUnwrapSol
            self.config.dynamicComputeUnitLimit = self.temp_dynamicCompute

            self.config.save_config()  # Сохранение конфигурации
        #     self.closed.emit()  # Сигнал закрытия
        #     event.accept()  # Закрыть окно
        # else:
        #     event.ignore()  # Отменить закрытие
        self.closed.emit()  # Сигнал закрытия
        event.accept()  # Закрыть окно
        
    def init_forms(self):
        # Локальные переменные для предварительных изменений
        self.temp_sol_mint = self.config.sol_mint
        self.temp_api_key = self.config.api_key
        self.temp_jupiter_url = self.config.jupiter_url
        self.temp_userpriority = self.config.usepriorityLevelWithMaxLamports
        self.temp_wallet_dir = self.config.wallets_dir
        self.temp_min_bps = self.config.dynamic_slippage["minBps"]
        self.temp_max_bps = self.config.dynamic_slippage["maxBps"]
        self.temp_wrapUnwrapSol = self.config.wrapUnwrapSOL
        self.temp_dynamicCompute = self.config.dynamicComputeUnitLimit
        # Инициализация полей
        self.sol_mint.setText(self.temp_sol_mint)
        self.api_key.setText(self.temp_api_key)
        self.jupiter_url_7.setText(self.temp_jupiter_url)
        self.userpriority.setText(str(lamports_to_sol(self.temp_userpriority)))
        self.wallet_dir.setText(self.temp_wallet_dir)
        self.MIN.setText(str(self.temp_min_bps))
        self.MAX.setText(str(self.temp_max_bps))

        # Инициализация чекбоксов
        self.wrapUnwrapSol.setChecked(self.temp_wrapUnwrapSol)
        self.dynamicCompute.setChecked(self.temp_dynamicCompute)
        
    def reset_data(self):
        self.config.reset_to_defaults()
        self.init_forms()