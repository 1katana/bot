import sys
from solana.rpc.api import Client
from solana.transaction import Transaction
from solders.instruction import Instruction
from solana.rpc.commitment import Confirmed
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solana.rpc.types import TxOpts
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QInputDialog, QTextEdit, QHBoxLayout, QLineEdit, QDialog, QDialogButtonBox
from PySide6.QtGui import QDoubleValidator, QColor
from PySide6.QtCore import Qt




class WalletManager(QMainWindow):
    def __init__(self):
        super().__init__()
        print("Initializing WalletManager...")  # Diagnostic message
        self.initUI()
        self.client = Client("https://api.devnet.solana.com")
        self.wallets = []
        self.master_wallet = None
        print("Initialization complete.")  # Diagnostic message

    def initUI(self):
        print("Setting up UI...")  # Diagnostic message
        self.setWindowTitle("Solana Wallet Manager")
        self.setGeometry(100, 100, 600, 500)

        layout = QVBoxLayout()

        self.statusLabel = QLabel("No wallets created")
        layout.addWidget(self.statusLabel)

        self.walletsText = QTextEdit()
        self.walletsText.setReadOnly(True)
        layout.addWidget(self.walletsText)

        buttonLayout = QHBoxLayout()

        importMasterWalletBtn = QPushButton("Import Master Wallet")
        importMasterWalletBtn.clicked.connect(self.import_master_wallet)
        buttonLayout.addWidget(importMasterWalletBtn)

        createWalletBtn = QPushButton("Create Wallets")
        createWalletBtn.clicked.connect(self.create_wallets)
        buttonLayout.addWidget(createWalletBtn)

        refreshBtn = QPushButton("Refresh")
        refreshBtn.clicked.connect(self.refresh_wallets)
        buttonLayout.addWidget(refreshBtn)

        layout.addLayout(buttonLayout)

        distributeSolBtn = QPushButton("Distribute SOL evenly")
        distributeSolBtn.clicked.connect(self.distribute_sol)
        layout.addWidget(distributeSolBtn)

        collectSolBtn = QPushButton("Collect SOL to Master Wallet")
        collectSolBtn.clicked.connect(self.collect_sol)
        layout.addWidget(collectSolBtn)

        buyTokenBtn = QPushButton("Buy Token")
        buyTokenBtn.clicked.connect(self.buy_token)
        layout.addWidget(buyTokenBtn)

        sellTokenBtn = QPushButton("Sell Token")
        sellTokenBtn.clicked.connect(self.sell_token)
        layout.addWidget(sellTokenBtn)

        deleteWalletBtn = QPushButton("Delete Wallets")
        deleteWalletBtn.clicked.connect(self.delete_wallets)
        layout.addWidget(deleteWalletBtn)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        print("UI setup complete.")  # Diagnostic message

    def import_master_wallet(self):
        print("Importing master wallet...")  # Diagnostic message
        self.dialog = QDialog(self)
        self.dialog.setWindowTitle("Import Master Wallet")

        layout = QVBoxLayout()

        label = QLabel("Enter your wallet secret key:")
        layout.addWidget(label)

        self.secretKeyInput = QLineEdit()
        layout.addWidget(self.secretKeyInput)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.handle_import_master_wallet)
        buttonBox.rejected.connect(self.dialog.reject)
        layout.addWidget(buttonBox)

        self.dialog.setLayout(layout)
        self.dialog.exec_()

    def handle_import_master_wallet(self):
        secret_key = self.secretKeyInput.text()
        if secret_key:
            try:
                
                self.master_wallet = Keypair.from_bytes()
                self.statusLabel.setText("Master wallet imported")
                self.update_wallets_display()
                print("Master wallet imported.")  # Diagnostic message
                self.dialog.accept()  # Close the dialog if import is successful
            except Exception as e:
                self.statusLabel.setText(f"Failed to import master wallet: {e}")
                print(f"Failed to import master wallet: {e}")  # Diagnostic message

    def create_wallets(self):
        print("Creating wallets...")  # Diagnostic message
        num_wallets, ok = QInputDialog.getInt(self, "Create Wallets", "Number of wallets to create (up to 30):", 1, 1, 30, 1)
        if ok:
            for _ in range(num_wallets):
                self.wallets.append(Keypair())
            self.update_wallets_display()
        print("Wallets created.")  # Diagnostic message

    def transfer_sol(self):
        recipient, ok = QInputDialog.getText(self, "Transfer SOL", "Enter recipient address:")
        amount, ok = QInputDialog.getDouble(self, "Transfer SOL", "Enter amount in SOL:", decimals=2)
        if ok:
            for wallet in self.wallets:
                txn = Transaction().add(
                    Instruction(
                        keys=[{"pubkey": wallet.public_key, "is_signer": True, "is_writable": True},
                              {"pubkey": Pubkey(recipient), "is_signer": False, "is_writable": True}],
                        program_id=Pubkey("11111111111111111111111111111111"),  # System Program ID
                        data=(int(amount * 10**9)).to_bytes(8, 'little')  # lamports
                    )
                )
                self.client.send_transaction(txn, wallet, opts=TxOpts(skip_preflight=True, skip_confirmation=False))
            self.statusLabel.setText(f"Transferred {amount} SOL to {recipient}")
            self.update_wallets_display()

    def distribute_sol(self):
        if not self.master_wallet:
            self.statusLabel.setText("Create a Master Wallet first")
            return

        try:
            total_sol = self.client.get_balance(self.master_wallet.public_key)["result"]["value"] / 10**9
            if total_sol == 0:
                self.statusLabel.setText("Master Wallet has no SOL to distribute")
                return

            amount_per_wallet = (total_sol / len(self.wallets)) * 10**9  # in lamports

            # Retry logic for fetching recent blockhash
            recent_blockhash = None
            for _ in range(3):  # Retry up to 3 times
                recent_blockhash_resp = self.client.get_recent_blockhash()
                if "result" in recent_blockhash_resp:
                    recent_blockhash = recent_blockhash_resp["result"]["value"]["blockhash"]
                    break
                else:
                    print("Retrying to get recent blockhash...")

            if not recent_blockhash:
                self.statusLabel.setText("Failed to get recent blockhash after multiple attempts")
                return

            for wallet in self.wallets:
                txn = Transaction(recent_blockhash=recent_blockhash).add(
                    Instruction(
                        keys=[{"pubkey": self.master_wallet.public_key, "is_signer": True, "is_writable": True},
                              {"pubkey": wallet.public_key, "is_signer": False, "is_writable": True}],
                        program_id=Pubkey("11111111111111111111111111111111"),  # System Program ID
                        data=(int(amount_per_wallet)).to_bytes(8, 'little')  # lamports
                    )
                )
                self.client.send_transaction(txn, self.master_wallet, opts=TxOpts(skip_preflight=True, skip_confirmation=False))

            self.statusLabel.setText(f"Distributed {total_sol} SOL evenly")
            self.update_wallets_display()
        except Exception as e:
            self.statusLabel.setText(f"Error distributing SOL: {e}")
            print(f"Error distributing SOL: {e}")  # Diagnostic message

    
    
    def collect_sol(self):
        if not self.master_wallet:
            self.statusLabel.setText("Create a Master Wallet first")
            return

        for wallet in self.wallets:
            balance = self.client.get_balance(wallet.public_key)["result"]["value"]
            if balance > 0:
                txn = Transaction().add(
                    Instruction(
                        keys=[{"pubkey": wallet.public_key, "is_signer": True, "is_writable": True},
                              {"pubkey": self.master_wallet.public_key, "is_signer": False, "is_writable": True}],
                        program_id=Pubkey("11111111111111111111111111111111"),  # System Program ID
                        data=(int(balance)).to_bytes(8, 'little')  # lamports
                    )
                )
                self.client.send_transaction(txn, wallet, opts=TxOpts(skip_preflight=True, skip_confirmation=False))

        self.statusLabel.setText("Collected SOL to Master Wallet")
        self.update_wallets_display()

    def buy_token(self):
        token_address, ok = QInputDialog.getText(self, "Buy Token", "Enter token address:")
        amount, ok = QInputDialog.getDouble(self, "Buy Token", "Enter amount to buy:", decimals=2)
        if ok:
            # Placeholder for actual token buying logic
            self.statusLabel.setText(f"Bought {amount} of token {token_address}")

    def sell_token(self):
        token_address, ok = QInputDialog.getText(self, "Sell Token", "Enter token address:")
        amount, ok = QInputDialog.getDouble(self, "Sell Token", "Enter amount to sell:", decimals=2)
        if ok:
            # Placeholder for actual token selling logic
            self.statusLabel.setText(f"Sold {amount} of token {token_address}")

    def delete_wallets(self):
        self.wallets.clear()
        self.master_wallet = None
        self.statusLabel.setText("All wallets deleted")
        self.update_wallets_display()

    def refresh_wallets(self):
        self.update_wallets_display()

    def update_wallets_display(self):
        wallet_info = ""
        if self.master_wallet:
            master_balance = self.client.get_balance(self.master_wallet.public_key)["result"]["value"] / 10**9  # convert to SOL
            master_private_key = self.master_wallet.secret_key.hex()
            wallet_info += f"<h3>Master Wallet</h3>Address: {self.master_wallet.public_key}<br>Balance: {master_balance} SOL<br>Private Key: {master_private_key}<hr>"

        for wallet in self.wallets:
            balance = self.client.get_balance(wallet.public_key)["result"]["value"] / 10**9  # convert to SOL
            private_key = wallet.secret_key.hex()
            status = "Ready" if balance > 0 else "Empty"
            color = "green" if balance > 0 else "red"
            wallet_info += f"Address: {wallet.public_key}<br>Balance: {balance} SOL<br>Private Key: {private_key}<br>Status: <span style='color:{color};'>{status}</span><hr>"
        self.walletsText.setHtml(wallet_info)

if __name__ == "__main__":
    print("Starting application...")  # Diagnostic message
    app = QApplication(sys.argv)
    mainWin = WalletManager()
    mainWin.show()
    print("Application started.")  # Diagnostic message
    sys.exit(app.exec_())
