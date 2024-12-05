import json
import os
import uuid
from solders.keypair import Keypair
from solders.system_program import TransferParams, transfer
from solders.message import MessageV0
from solders.hash import Hash
from solders.transaction import VersionedTransaction
from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey

class WalletManager:
    def __init__(self, wallets_dir="wallets"):
        self.wallets_dir = wallets_dir
        os.makedirs(self.wallets_dir, exist_ok=True)
        self.wallets = self.load_wallets()

    def add_wallet(self,secret_key:str):
        
        key = Keypair.from_bytes(bytes.fromhex(secret_key))

        self.save_wallet(key,"master_wallet")
        self.load_wallets()
        
        self.master_wallet= key
    
    
    def load_wallets(self):
        wallets = {}
        if os.path.exists(self.wallets_dir) and os.path.isdir(self.wallets_dir):
            for file_name in os.listdir(self.wallets_dir):
                file_path = os.path.join(self.wallets_dir, file_name)
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    wallets[file_name] = Keypair.from_bytes(data)
        return wallets

    def save_wallet(self, keypair: Keypair, name: str):
        file_name = f"{name}.json"
        file_path = os.path.join(self.wallets_dir, file_name)

        # Проверка на наличие файла с таким именем
        if os.path.exists(file_path):
            # Генерация нового уникального имени
            suffix = 1
            while os.path.exists(file_path):
                file_name = f"{name}_{suffix}.json"
                file_path = os.path.join(self.wallets_dir, file_name)
                suffix += 1

        
        with open(file_path, 'w') as file:
            file.write(keypair.to_json())
        self.wallets[file_name] = keypair

    def generate_wallet(self, name: str = None):
        if name is None:
            name = str(uuid.uuid4())
        keypair = Keypair()
        self.save_wallet(keypair, name)
        return keypair

    def get_wallet(self, name: str):
        file_name = f"{name}.json"
        return self.wallets.get(file_name)

    def set_master_wallet(self, name: str):
        self.master_wallet = self.get_wallet(name)



        
if __name__=="__main__":
    
    wallet=WalletManager()
    
    