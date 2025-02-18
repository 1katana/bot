from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QTextEdit, QFormLayout
)
from PySide6.QtGui import QPixmap
import sys
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject,QUrl, Signal, Slot, Qt)
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QApplication, QVBoxLayout, QMainWindow, QPushButton, QMessageBox, QWidget
from app.ui.design.setting import Ui_Form
from app.managers.config import Config
from app.utils.converter import *
from app.utils.parser_form import *
from app.PumpFun.pumpFun import PumpFunTokenCreator, TokenCreator
import asyncio

class TokenCreationState(QObject):
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

class TokenCreationForm(QWidget):
    closed = Signal()   # Сигнал для уведомления о закрытии окна

    def __init__(self, token_creation_state: TokenCreationState, pump_fun_token_creator: PumpFunTokenCreator):
        super().__init__()
        self.setWindowTitle("Создание токена")
        self.setGeometry(100, 100, 400, 500)

        self.token_creation_state = token_creation_state
        self.pump_fun_token_creator = pump_fun_token_creator

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.name_input = QLineEdit()
        self.symbol_input = QLineEdit()
        self.description_input = QTextEdit()
        self.twitter_input = QLineEdit()
        self.telegram_input = QLineEdit()
        self.website_input = QLineEdit()

        form_layout.addRow("Название:", self.name_input)
        form_layout.addRow("Символ:", self.symbol_input)
        form_layout.addRow("Описание:", self.description_input)
        form_layout.addRow("Twitter:", self.twitter_input)
        form_layout.addRow("Telegram:", self.telegram_input)
        form_layout.addRow("Website:", self.website_input)

        self.image_label = QLabel("[Нет изображения]")
        self.image_label.setFixedSize(200, 200)

        self.image_button = QPushButton("Выбрать изображение")
        self.image_button.clicked.connect(self.choose_image)

        self.create_button = QPushButton("Проверить токен")
        self.create_button.clicked.connect(lambda: asyncio.create_task(self.validate_token()))

        layout.addLayout(form_layout)
        layout.addWidget(self.image_label)
        layout.addWidget(self.image_button)
        layout.addWidget(self.create_button)

        self.setLayout(layout)
        self.image_path = None

        self.closed.connect(lambda: self.token_creation_state.set_open(False))

        # Подключаем сигналы для обновления данных в реальном времени
        self.name_input.textChanged.connect(self.update_token_data)
        self.symbol_input.textChanged.connect(self.update_token_data)
        self.description_input.textChanged.connect(self.update_token_data)
        self.twitter_input.textChanged.connect(self.update_token_data)
        self.telegram_input.textChanged.connect(self.update_token_data)
        self.website_input.textChanged.connect(self.update_token_data)
        

        self.pump_fun_token_creator.tokenDataChanged.connect(self.update_form_data)
        self.update_form_data(self.pump_fun_token_creator.token_data)

    def choose_image(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Выберите изображение", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            self.image_path = file_path
            pixmap = QPixmap(file_path)
            self.image_label.setPixmap(pixmap.scaled(200, 200))
            self.update_token_data()


    async def validate_token(self):
        metadata = await self.pump_fun_token_creator.validate_token_metadata(
            self.pump_fun_token_creator.token_data["name"],
            self.pump_fun_token_creator.token_data["symbol"],
            self.pump_fun_token_creator.token_data["description"],
            self.pump_fun_token_creator.token_data["image_path"],
            self.pump_fun_token_creator.token_data["social_links"]
        )

        if metadata:
            print("Можно создовать токен!!!")
        else:
            print("Ошибка при проверке метаданных токена.")
            
        # signer_keypair = self.pump_fun_token_creator._generate_token_keypair()
        #     token_creator = await self.pump_fun_token_creator.create_token_transaction(signer_keypair, metadata)
        #     if token_creator:
        #         print("Токен успешно создан:", token_creator)
        #     else:
        #         print("Ошибка при создании токена.")

    def update_token_data(self):
        """
        Обновляет данные токена в PumpFunTokenCreator при каждом изменении в полях.
        """
        token_data = {
            "name": self.name_input.text(),
            "symbol": self.symbol_input.text(),
            "description": self.description_input.toPlainText(),
            "social_links": {
                "twitter": self.twitter_input.text(),
                "telegram": self.telegram_input.text(),
                "website": self.website_input.text()
            },
            "image_path": self.image_path
        }
        self.pump_fun_token_creator.token_data = token_data

    def update_form_data(self, token_data: dict):
        """
        Обновляет данные в полях формы при изменении данных токена.
        """
        self.name_input.setText(token_data["name"])
        self.symbol_input.setText(token_data["symbol"])
        self.description_input.setPlainText(token_data["description"])
        self.twitter_input.setText(token_data["social_links"]["twitter"])
        self.telegram_input.setText(token_data["social_links"]["telegram"])
        self.website_input.setText(token_data["social_links"]["website"])
        self.image_path = token_data["image_path"]
        if self.image_path:
            pixmap = QPixmap(self.image_path)
            self.image_label.setPixmap(pixmap.scaled(200, 200))

    def closeEvent(self, event):
        """
        Обработчик закрытия окна.
        """
        self.closed.emit()
        event.accept()  
        