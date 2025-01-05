import asyncio
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, 
    QLabel, QLineEdit, QInputDialog, QMessageBox
)
from PySide6.QtCore import QTimer, QEventLoop
from solana_manager import SolanaManager

class SolanaManagerGUI(QMainWindow):
    def __init__(self, solana_manager:SolanaManager):
        super().__init__()
        self.solana_manager = solana_manager

        self.setWindowTitle("Solana Manager")
        self.setGeometry(100, 100, 600, 400)

        # Основной виджет
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Макет
        layout = QVBoxLayout()

        # Кнопки
        self.status_label = QLabel("Статус: Готов")
        layout.addWidget(self.status_label)

        load_wallets_btn = QPushButton("Загрузить кошельки из директории")
        load_wallets_btn.clicked.connect(self.load_wallets)
        layout.addWidget(load_wallets_btn)

        create_wallet_btn = QPushButton("Создать новые кошельки")
        create_wallet_btn.clicked.connect(self.create_wallets)
        layout.addWidget(create_wallet_btn)

        add_wallet_btn = QPushButton("Добавить кошелек по секретному ключу")
        add_wallet_btn.clicked.connect(self.add_wallet)
        layout.addWidget(add_wallet_btn)

        set_master_btn = QPushButton("Назначить мастер-кошелек")
        set_master_btn.clicked.connect(self.set_master_wallet)
        layout.addWidget(set_master_btn)

        buy_tokens_btn = QPushButton("Купить токены")
        buy_tokens_btn.clicked.connect(self.buy_tokens)
        layout.addWidget(buy_tokens_btn)

        sell_tokens_btn = QPushButton("Продать токены")
        sell_tokens_btn.clicked.connect(self.sell_tokens)
        layout.addWidget(sell_tokens_btn)

        distribute_funds_btn = QPushButton("Распределить средства")
        distribute_funds_btn.clicked.connect(self.distribute_funds)
        layout.addWidget(distribute_funds_btn)

        collect_funds_btn = QPushButton("Собрать средства на мастер-кошелек")
        collect_funds_btn.clicked.connect(self.collect_funds)
        layout.addWidget(collect_funds_btn)

        main_widget.setLayout(layout)

    def async_run(self, coroutine):
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # Для интеграции с GUI
            asyncio.run_coroutine_threadsafe(coroutine, loop)
        else:
            loop.run_until_complete(coroutine)

    def update_status(self, message):
        self.status_label.setText(f"Статус: {message}")

    def show_error(self, message):
        QMessageBox.critical(self, "Ошибка", message)

    def get_input(self, title, label):
        text, ok = QInputDialog.getText(self, title, label)
        return text if ok else None

    def load_wallets(self):
        self.async_run(self.solana_manager.load_from_dir())
        self.update_status("Кошельки загружены.")

    def create_wallets(self):
        num = self.get_input("Создать кошельки", "Введите количество кошельков:")
        if num and num.isdigit():
            self.async_run(self.solana_manager.create_wallets(int(num)))
            self.update_status(f"Создано {num} кошельков.")
        else:
            self.show_error("Неверное количество.")

    def add_wallet(self):
        secret_key = self.get_input("Добавить кошелек", "Введите секретный ключ:")
        if secret_key:
            self.async_run(self.solana_manager.add_wallet(secret_key))
            self.update_status("Кошелек добавлен.")

    def set_master_wallet(self):
        wallet_address = self.get_input("Мастер-кошелек", "Введите адрес кошелька:")
        if wallet_address:
            self.async_run(self.solana_manager.set_master_wallet(wallet_address, True))
            self.update_status("Мастер-кошелек установлен.")

    def buy_tokens(self):
        amount = self.get_input("Купить токены", "Введите сумму в lamports:")
        if amount and amount.isdigit():
            self.async_run(self.solana_manager.buy_token(int(amount), self.confirmation_callback))
            self.update_status("Токены куплены.")

    def sell_tokens(self):
        self.async_run(self.solana_manager.sell_token(self.confirmation_callback))
        self.update_status("Токены проданы.")

    def distribute_funds(self):
        amount = self.get_input("Распределить средства", "Введите сумму на кошелек (-1 для равномерного):")
        if amount and amount.isdigit():
            self.async_run(self.solana_manager.distribute_funds(int(amount)))
            self.update_status("Средства распределены.")

    def collect_funds(self):
        self.async_run(self.solana_manager.collect_funds_to_master())
        self.update_status("Средства собраны.")

    async def confirmation_callback(self, message: str) -> bool:
        reply = QMessageBox.question(self, "Подтверждение", message, 
                                     QMessageBox.Yes | QMessageBox.No)
        return reply == QMessageBox.Yes


if __name__ == "__main__":
    app = QApplication([])

    # Инициализация SolanaManager (асинхронная часть)
    async def initialize():
        manager = await SolanaManager.create()
        return manager

    solana_manager = asyncio.run(initialize())
    gui = SolanaManagerGUI(solana_manager)
    gui.show()
    app.exec()
